import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import ANALYTICS_MATCH_TYPE_PARQUET, MATCH_SUMMARY_PARQUET, ANOMALIES_PARQUET
from src.cassandra_client import CassandraClient

def load_parquet_into_cassandra():
    """
    Reads processed Parquet outputs and loads them into Apache Cassandra / Persistent Storage.
    """
    print(">>> Đang nạp lại dữ liệu từ Parquet vào Apache Cassandra...")
    client = CassandraClient()
    
    if ANALYTICS_MATCH_TYPE_PARQUET.exists():
        df_modes = pd.read_parquet(ANALYTICS_MATCH_TYPE_PARQUET)
        client.insert_match_type_analytics(df_modes.to_dict(orient="records"))
        print(f"  + Đã nạp {len(df_modes)} chế độ chơi vào analytics_by_match_type.")

    if MATCH_SUMMARY_PARQUET.exists():
        df_matches = pd.read_parquet(MATCH_SUMMARY_PARQUET).head(1000)
        client.insert_match_summaries(df_matches.to_dict(orient="records"))
        print(f"  + Đã nạp {len(df_matches)} trận đấu vào match_summary_by_id.")

    if ANOMALIES_PARQUET.exists():
        df_anom = pd.read_parquet(ANOMALIES_PARQUET).head(2000)
        client.insert_suspicious_records(run_id="quick", rows=df_anom.to_dict(orient="records"))
        print(f"  + Đã nạp {len(df_anom)} bản ghi bất thường vào suspicious_records_by_run.")

    print(">>> Hoàn tất nạp dữ liệu vào cơ sở dữ liệu!")

if __name__ == "__main__":
    load_parquet_into_cassandra()
