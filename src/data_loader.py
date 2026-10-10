import logging
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)

logger = logging.getLogger(__name__)

# Explicit PUBG Schema to avoid costly schema inference on 4.4M+ rows
PUBG_SCHEMA = StructType([
    StructField("Id", StringType(), False),
    StructField("groupId", StringType(), False),
    StructField("matchId", StringType(), False),
    StructField("assists", IntegerType(), True),
    StructField("boosts", IntegerType(), True),
    StructField("damageDealt", DoubleType(), True),
    StructField("DBNOs", IntegerType(), True),
    StructField("headshotKills", IntegerType(), True),
    StructField("heals", IntegerType(), True),
    StructField("killPlace", IntegerType(), True),
    StructField("killPoints", IntegerType(), True),
    StructField("kills", IntegerType(), True),
    StructField("killStreaks", IntegerType(), True),
    StructField("longestKill", DoubleType(), True),
    StructField("matchDuration", IntegerType(), True),
    StructField("matchType", StringType(), True),
    StructField("maxPlace", IntegerType(), True),
    StructField("numGroups", IntegerType(), True),
    StructField("rankPoints", IntegerType(), True),
    StructField("revives", IntegerType(), True),
    StructField("rideDistance", DoubleType(), True),
    StructField("roadKills", IntegerType(), True),
    StructField("swimDistance", DoubleType(), True),
    StructField("teamKills", IntegerType(), True),
    StructField("vehicleDestroys", IntegerType(), True),
    StructField("walkDistance", DoubleType(), True),
    StructField("weaponsAcquired", IntegerType(), True),
    StructField("winPoints", IntegerType(), True),
    StructField("winPlacePerc", DoubleType(), True),
])

def load_raw_dataset(spark: SparkSession, file_path: Path) -> DataFrame:
    """
    Loads raw PUBG CSV file into a PySpark DataFrame with strict schema enforcement.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Tập tin dữ liệu không tồn tại: {file_path}")

    logger.info("Đang đọc dữ liệu PUBG từ: %s", file_path)
    df = (
        spark.read
        .option("header", "true")
        .schema(PUBG_SCHEMA)
        .csv(str(file_path))
    )
    
    return df
