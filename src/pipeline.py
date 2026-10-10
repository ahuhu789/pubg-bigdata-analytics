import argparse
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import (
    RAW_FULL_CSV, RAW_QUICK_CSV, CLEANED_PARQUET,
    ANALYTICS_MATCH_TYPE_PARQUET, MATCH_SUMMARY_PARQUET,
    ANOMALIES_PARQUET, KMEANS_K, ANOMALY_PERCENTILE_THRESHOLD,
    RANDOM_SEED, get_spark_session
)
from src.data_loader import load_raw_dataset
from src.preprocessing import clean_and_validate_data
from src.match_analytics import (
    compute_match_type_analytics, compute_match_summary,
    compute_combat_correlations
)
from src.feature_engineering import (
    engineer_gameplay_features, prepare_feature_vectors
)
from src.anomaly_detection import fit_kmeans_and_detect_anomalies
from src.cassandra_client import CassandraClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PUBG-Pipeline")

def run_pipeline(mode: str = "quick"):
    """
    Executes the end-to-end Big Data pipeline for PUBG esports analytics
    and explainable anomaly detection.
    """
    start_total_time = time.time()
    run_id = f"run_{mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger.info("=================================================================")
    logger.info("KHỞI ĐỘNG BIG DATA PIPELINE [PUBG ANALYTICS & ANOMALY DETECTION]")
    logger.info("Chế độ: %s | Run ID: %s", mode.upper(), run_id)
    logger.info("=================================================================")

    # 1. Chọn file dữ liệu theo chế độ
    target_csv = RAW_QUICK_CSV if mode == "quick" else RAW_FULL_CSV
    if not target_csv.exists():
        if mode == "quick" and RAW_FULL_CSV.exists():
            logger.warning("File quick chưa có, tiến hành đọc từ full CSV...")
            target_csv = RAW_FULL_CSV
        else:
            raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {target_csv}")

    # 2. Khởi tạo PySpark Session
    logger.info("[BƯỚC 1/7] Khởi tạo Apache Spark Session tối ưu hóa cho Windows...")
    spark = get_spark_session(app_name=f"PUBG-Esports-{mode.capitalize()}")

    try:
        # 3. Nạp dữ liệu thô
        t0 = time.time()
        logger.info("[BƯỚC 2/7] Nạp dữ liệu thô với PySpark Schema...")
        raw_df = load_raw_dataset(spark, target_csv)
        load_time = time.time() - t0
        logger.info("Nạp dữ liệu hoàn tất trong %.2f giây.", load_time)

        # 4. Tiền xử lý và làm sạch dữ liệu
        t0 = time.time()
        logger.info("[BƯỚC 3/7] Tiền xử lý, kiểm tra chất lượng và bảo toàn điểm cực trị...")
        cleaned_df, quality_report = clean_and_validate_data(raw_df)
        cleaned_df.cache()
        clean_time = time.time() - t0
        logger.info("Làm sạch dữ liệu hoàn tất trong %.2f giây.", clean_time)

        # 5. Phân tích thống kê trận đấu & chế độ chơi
        t0 = time.time()
        logger.info("[BƯỚC 4/7] Phân tích thống kê tổng hợp trận đấu bằng PySpark...")
        match_type_df = compute_match_type_analytics(cleaned_df)
        match_summary_df = compute_match_summary(cleaned_df)
        correlations = compute_combat_correlations(cleaned_df)
        analytics_time = time.time() - t0
        logger.info("Phân tích hoàn tất trong %.2f giây.", analytics_time)

        # 6. Kỹ nghệ đặc trưng
        t0 = time.time()
        logger.info("[BƯỚC 5/7] Kỹ nghệ đặc trưng hành vi và vector chuẩn hóa...")
        feat_df = engineer_gameplay_features(cleaned_df)
        vector_df = prepare_feature_vectors(feat_df)
        vector_df.cache()
        feat_time = time.time() - t0
        logger.info("Tạo đặc trưng hoàn tất trong %.2f giây.", feat_time)

        # 7. Phát hiện bất thường bằng PySpark MLlib KMeans
        t0 = time.time()
        logger.info("[BƯỚC 6/7] Huấn luyện KMeans và phát hiện bất thường không giám sát...")
        final_df, model_metrics = fit_kmeans_and_detect_anomalies(
            vector_df,
            k=KMEANS_K,
            percentile_threshold=ANOMALY_PERCENTILE_THRESHOLD,
            random_seed=RANDOM_SEED
        )
        ml_time = time.time() - t0
        logger.info("Mô hình học máy hoàn tất trong %.2f giây.", ml_time)

        # 8. Lưu kết quả Parquet
        logger.info("Đang ghi dữ liệu Parquet đã xử lý...")
        match_type_df.write.mode("overwrite").parquet(str(ANALYTICS_MATCH_TYPE_PARQUET))
        match_summary_df.write.mode("overwrite").parquet(str(MATCH_SUMMARY_PARQUET))
        
        # Chỉ lưu các bản ghi bị đánh dấu hoặc mẫu kiểm tra để tiết kiệm dung lượng
        suspicious_df = final_df.filter(final_df.is_anomalous == True)
        suspicious_df.write.mode("overwrite").parquet(str(ANOMALIES_PARQUET))

        # 9. Nạp kết quả vào Apache Cassandra
        t0 = time.time()
        logger.info("[BƯỚC 7/7] Nạp kết quả phân tích vào Apache Cassandra...")
        cassandra = CassandraClient()
        
        # Nạp dữ liệu chế độ chơi
        match_type_rows = [r.asDict() for r in match_type_df.collect()]
        cassandra.insert_match_type_analytics(match_type_rows)

        # Nạp dữ liệu trận đấu (lấy mẫu 500 trận nếu dataset lớn)
        match_summary_rows = [r.asDict() for r in match_summary_df.limit(1000).collect()]
        cassandra.insert_match_summaries(match_summary_rows)

        # Nạp dữ liệu cảnh báo bất thường
        suspicious_rows = [r.asDict() for r in suspicious_df.limit(2000).collect()]
        cassandra.insert_suspicious_records(run_id=mode, rows=suspicious_rows)

        # Ghi log lượt chạy pipeline
        total_exec_time = time.time() - start_total_time
        run_metadata = {
            "run_id": run_id,
            "mode": mode,
            "input_records": quality_report["raw_count"],
            "cleaned_records": quality_report["cleaned_count"],
            "matches_count": len(match_summary_rows),
            "anomalies_detected": model_metrics["anomalies_detected"],
            "execution_time_sec": round(total_exec_time, 2),
            "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS"
        }
        cassandra.insert_pipeline_run(run_metadata)
        db_time = time.time() - t0
        logger.info("Nạp dữ liệu Cassandra hoàn tất trong %.2f giây.", db_time)

        logger.info("=================================================================")
        logger.info("PIPELINE HOÀN THÀNH XUẤT SẮC! Tổng thời gian: %.2f giây", total_exec_time)
        logger.info("Số bản ghi đánh giá: %d | Số đối tượng bất thường: %d", quality_report["cleaned_count"], model_metrics["anomalies_detected"])
        logger.info("=================================================================")

        return {
            "run_metadata": run_metadata,
            "quality_report": quality_report,
            "model_metrics": model_metrics,
            "correlations": correlations,
            "timing": {
                "load_time": round(load_time, 2),
                "clean_time": round(clean_time, 2),
                "analytics_time": round(analytics_time, 2),
                "feat_time": round(feat_time, 2),
                "ml_time": round(ml_time, 2),
                "db_time": round(db_time, 2),
                "total_time": round(total_exec_time, 2)
            }
        }

    finally:
        logger.info("Đang dừng SparkSession...")
        spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PUBG Big Data Pipeline")
    parser.add_argument("--mode", choices=["quick", "full"], default="quick", help="Execution mode: quick or full")
    args = parser.parse_args()
    run_pipeline(mode=args.mode)
