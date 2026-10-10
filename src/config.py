import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession

# Base project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
TOOLS_DIR = PROJECT_ROOT / "tools"
HADOOP_DIR = TOOLS_DIR / "hadoop"

# Raw and processed data paths
RAW_FULL_CSV = DATA_RAW_DIR / "train_V2.csv"
RAW_QUICK_CSV = DATA_RAW_DIR / "train_quick.csv"
CLEANED_PARQUET = DATA_PROCESSED_DIR / "cleaned_data.parquet"
ANALYTICS_MATCH_TYPE_PARQUET = DATA_PROCESSED_DIR / "analytics_by_match_type.parquet"
MATCH_SUMMARY_PARQUET = DATA_PROCESSED_DIR / "match_summary.parquet"
ANOMALIES_PARQUET = DATA_PROCESSED_DIR / "suspicious_records.parquet"

# Cassandra configuration
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "pubg_analytics")

# Modeling & Big Data parameters
KMEANS_K = 4
ANOMALY_PERCENTILE_THRESHOLD = 99.5
RANDOM_SEED = 42

def configure_environment():
    """Sets necessary Windows environment variables for PySpark and Hadoop."""
    # Java configuration
    jdk_path = Path(r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot")
    if jdk_path.exists():
        os.environ["JAVA_HOME"] = str(jdk_path)
    
    # Hadoop / winutils configuration
    if HADOOP_DIR.exists():
        os.environ["HADOOP_HOME"] = str(HADOOP_DIR)
        hadoop_bin = str(HADOOP_DIR / "bin")
        if hadoop_bin not in os.environ.get("PATH", ""):
            os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ.get("PATH", "")

    # Python executable for PySpark workers
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

def get_spark_session(app_name="PUBG-BigData-Pipeline", master="local[4]", driver_memory="4g"):
    """
    Creates and tunes an Apache Spark Session optimized for local execution.
    """
    configure_environment()
    
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.default.parallelism", "8")
        .config("spark.python.worker.reuse", "true")
        .config("spark.ui.showConsoleProgress", "true")
    )
    
    return builder.getOrCreate()
