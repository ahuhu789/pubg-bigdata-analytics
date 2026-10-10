import logging
from typing import Dict, Any, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, expr, percentile_approx, when, round as spark_round,
    concat, concat_ws, lit, array, array_remove, sqrt
)
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.functions import vector_to_array

logger = logging.getLogger(__name__)

def fit_kmeans_and_detect_anomalies(
    df: DataFrame,
    k: int = 4,
    percentile_threshold: float = 99.5,
    random_seed: int = 42
) -> Tuple[DataFrame, Dict[str, Any]]:
    """
    Performs unsupervised anomaly detection using PySpark MLlib KMeans.
    
    Optimizations:
    - 100% Native Spark SQL Catalyst execution for Euclidean distance and explanations.
    - Zero Python UDF serialization overhead, immune to worker socket timeouts.
    - Accurately computes cluster centroids and anomaly scoring.
    """
    logger.info("Đang huấn luyện mô hình PySpark MLlib KMeans (k=%d)...", k)
    
    kmeans = KMeans(k=k, seed=random_seed, featuresCol="features", predictionCol="cluster_id")
    model = kmeans.fit(df)
    
    # 1. Đánh giá chất lượng phân cụm (Silhouette Score)
    evaluator = ClusteringEvaluator(featuresCol="features", predictionCol="cluster_id", metricName="silhouette")
    predictions = model.transform(df)
    silhouette = evaluator.evaluate(predictions)
    logger.info("Điểm Silhouette của phân cụm: %.4f", silhouette)
    
    raw_centers = model.clusterCenters()
    centers = [c.tolist() if hasattr(c, "tolist") else list(c) for c in raw_centers]
    num_features = len(centers[0])
    logger.info("Tâm các cụm đặc trưng (Clusters: %d, Số chiều: %d): Đã tính toán.", len(centers), num_features)

    # 2. Tính khoảng cách Euclidean thuần túy bằng Native Catalyst
    pred_with_arr = predictions.withColumn("feat_arr", vector_to_array("features"))
    
    # Xây dựng biểu thức khoảng cách cho từng cluster_id
    dist_expr = None
    for cluster_idx, center_vec in enumerate(centers):
        sum_sq = lit(0.0)
        for dim_idx in range(num_features):
            diff = col("feat_arr")[dim_idx] - lit(float(center_vec[dim_idx]))
            sum_sq = sum_sq + (diff * diff)
        cluster_dist = sqrt(sum_sq)
        
        if dist_expr is None:
            dist_expr = when(col("cluster_id") == cluster_idx, cluster_dist)
        else:
            dist_expr = dist_expr.when(col("cluster_id") == cluster_idx, cluster_dist)
    
    dist_expr = dist_expr.otherwise(lit(0.0))
    df_with_dist = pred_with_arr.withColumn("centroid_distance", spark_round(dist_expr, 4))

    # 3. Tính ngưỡng phân vị (ví dụ 99.5%) của khoảng cách
    perc_fraction = percentile_threshold / 100.0
    threshold_row = df_with_dist.select(
        percentile_approx("centroid_distance", perc_fraction).alias("threshold_dist"),
        expr("max(centroid_distance)").alias("max_dist"),
        expr("avg(centroid_distance)").alias("avg_dist")
    ).collect()[0]
    
    dist_threshold = float(threshold_row["threshold_dist"] or 3.5)
    max_dist = float(threshold_row["max_dist"] or 10.0)
    avg_dist = float(threshold_row["avg_dist"] or 1.0)
    
    logger.info(
        "Khoảng cách trung bình: %.4f | Ngưỡng phân vị (%.1f%%): %.4f | Khoảng cách cực đại: %.4f",
        avg_dist, percentile_threshold, dist_threshold, max_dist
    )

    # 4. Tính toán Anomaly Score (thang điểm 0 - 100)
    df_scored = df_with_dist.withColumn(
        "anomaly_score",
        spark_round(
            (col("centroid_distance") / lit(max(max_dist, 1.0))) * 60.0 +
            (col("flag_teleport") * 25.0) +
            (col("flag_aimbot") * 25.0) +
            (col("flag_extreme_range") * 20.0) +
            (col("flag_speed") * 20.0),
            2
        )
    )

    # 5. Phân loại đối tượng và gán nhãn mức độ cảnh báo
    df_flagged = df_scored.withColumn(
        "is_anomalous",
        when(
            (col("centroid_distance") >= dist_threshold) |
            (col("flag_teleport") == 1) |
            (col("flag_aimbot") == 1) |
            (col("flag_extreme_range") == 1),
            True
        ).otherwise(False)
    ).withColumn(
        "warning_level",
        when(col("anomaly_score") >= 65.0, "NGUY CƠ CAO (HIGH)")
        .when(col("anomaly_score") >= 35.0, "CẦN KIỂM TRA (MEDIUM)")
        .otherwise("BÌNH THƯỜNG (LOW)")
    )

    # 6. Tạo phần giải thích chi tiết (Explainability) bằng biểu thức Spark SQL gốc
    reason_expr = concat_ws(" | ",
        when(col("flag_teleport") == 1, concat(lit("[Dịch chuyển] "), col("kills"), lit(" hạ gục nhưng đi bộ chỉ "), spark_round(col("walkDistance"), 1), lit("m"))),
        when(col("flag_aimbot") == 1, concat(lit("[Aimbot] Tỷ lệ Headshot "), spark_round(col("headshotRate") * 100.0, 1), lit("% ("), col("kills"), lit(" hạ gục)"))),
        when(col("flag_extreme_range") == 1, concat(lit("[Bắn xa phi lý] Hạ gục ở cự ly "), spark_round(col("longestKill"), 1), lit("m"))),
        when(col("flag_speed") == 1, concat(lit("[Tốc độ bất thường] Đi bộ "), spark_round(col("walkDistance"), 1), lit("m"))),
        when(col("centroid_distance") >= dist_threshold, concat(lit("[Độ lệch tâm cụm] Điểm khoảng cách: "), spark_round(col("centroid_distance"), 2), lit(" (Kills: "), col("kills"), lit(", Sát thương: "), spark_round(col("damageDealt"), 1), lit(")"))),
        when((col("warning_level") != "BÌNH THƯỜNG (LOW)") & (col("anomaly_score") >= 35.0), concat(lit("[Chỉ số nghi vấn] Điểm bất thường: "), spark_round(col("anomaly_score"), 1)))
    )

    df_with_reasons = df_flagged.withColumn(
        "reason",
        when((reason_expr == "") | (reason_expr.isNull()), lit("Hành vi thi đấu phù hợp chuẩn"))
        .otherwise(reason_expr)
    )

    # Loại bỏ các cột phụ trợ vector để tương thích hoàn toàn với Parquet và cơ sở dữ liệu
    df_final = df_with_reasons.drop("raw_features", "features", "feat_arr")

    # Thống kê kết quả thực tế
    total_records = df_final.count()
    flagged_records = df_final.filter(col("is_anomalous") == True).count()
    high_risk_records = df_final.filter(col("warning_level") == "NGUY CƠ CAO (HIGH)").count()

    metrics = {
        "k_clusters": k,
        "silhouette_score": round(silhouette, 4),
        "distance_threshold": round(dist_threshold, 4),
        "total_evaluated": total_records,
        "anomalies_detected": flagged_records,
        "high_risk_count": high_risk_records,
        "anomaly_rate_percent": round((flagged_records / total_records) * 100, 3) if total_records > 0 else 0.0,
        "cluster_centers": centers
    }

    logger.info(
        "Đánh giá hoàn tất: %d / %d bản ghi có dấu hiệu bất thường (Tỷ lệ: %.3f%%)",
        flagged_records, total_records, metrics["anomaly_rate_percent"]
    )

    return df_final, metrics
