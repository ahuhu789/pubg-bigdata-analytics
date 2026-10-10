import logging
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, round as spark_round
from pyspark.ml.feature import VectorAssembler, StandardScaler

logger = logging.getLogger(__name__)

# Numerical features chosen for statistical anomaly modeling
FEATURE_COLS: List[str] = [
    "kills",
    "damageDealt",
    "headshotKills",
    "longestKill",
    "totalDistance",
    "headshotRate",
    "damagePerKill",
    "killsPerWalkKm"
]

def engineer_gameplay_features(df: DataFrame) -> DataFrame:
    """
    Computes domain-specific gameplay features and anti-cheat statistical flags.
    """
    logger.info("Đang tạo các đặc trưng hành vi và hiệu suất thi đấu...")

    feat_df = (
        df
        # 1. Tổng quãng đường di chuyển (bộ + xe + bơi)
        .withColumn("totalDistance", spark_round(col("walkDistance") + col("rideDistance") + col("swimDistance"), 2))
        
        # 2. Tỷ lệ Headshot (Headshot Rate)
        .withColumn(
            "headshotRate",
            spark_round(
                when(col("kills") > 0, col("headshotKills") / col("kills")).otherwise(0.0),
                4
            )
        )
        
        # 3. Sát thương trung bình trên mỗi mạng hạ gục (Damage Per Kill)
        .withColumn(
            "damagePerKill",
            spark_round(
                when(col("kills") > 0, col("damageDealt") / col("kills")).otherwise(col("damageDealt")),
                2
            )
        )
        
        # 4. Tỷ lệ Kill / Km đi bộ (phát hiện hành vi đứng yên hoặc dịch chuyển hạ sát)
        .withColumn(
            "killsPerWalkKm",
            spark_round(
                col("kills") / ((col("walkDistance") / 1000.0) + 0.001),
                4
            )
        )
        
        # 5. Các cờ dấu hiệu bất thường theo logic vật lý và luật chơi PUBG
        .withColumn(
            "flag_teleport",
            when((col("kills") >= 5) & (col("walkDistance") < 100.0), 1).otherwise(0)
        )
        .withColumn(
            "flag_aimbot",
            when((col("kills") >= 8) & (col("headshotRate") >= 0.85), 1).otherwise(0)
        )
        .withColumn(
            "flag_speed",
            when(col("walkDistance") > 13000.0, 1).otherwise(0)
        )
        .withColumn(
            "flag_extreme_range",
            when(col("longestKill") > 1000.0, 1).otherwise(0)
        )
    )

    return feat_df

def prepare_feature_vectors(df: DataFrame) -> DataFrame:
    """
    Assembles numerical features into vectors and scales them for Spark MLlib KMeans.
    """
    logger.info("Đang chuẩn hóa vector đặc trưng bằng VectorAssembler và StandardScaler...")
    
    assembler = VectorAssembler(
        inputCols=FEATURE_COLS,
        outputCol="raw_features",
        handleInvalid="skip"
    )
    
    assembled_df = assembler.transform(df)
    
    scaler = StandardScaler(
        inputCol="raw_features",
        outputCol="features",
        withStd=True,
        withMean=True
    )
    
    scaler_model = scaler.fit(assembled_df)
    scaled_df = scaler_model.transform(assembled_df)
    
    return scaled_df
