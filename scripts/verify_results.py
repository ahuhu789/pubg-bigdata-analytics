import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from src.cassandra_client import CassandraClient

def main():
    client = CassandraClient()
    print("================ SYSTEM STATUS ================")
    status = client.get_system_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n================ LATEST PIPELINE RUN ================")
    run = client.get_latest_pipeline_run()
    if run:
        for k, v in run.items():
            print(f"  {k}: {v}")

    print("\n================ TOP MATCH TYPES (BY PLAYERS) ================")
    modes = client.get_match_type_analytics()
    if not modes.empty:
        print(modes[["match_type", "total_matches", "total_players", "avg_duration_sec", "avg_kills", "max_kills", "avg_damage"]].to_string(index=False))

    print("\n================ TOP FLAGGED ANOMALIES ================")
    anomalies = client.get_suspicious_records(limit=10)
    if not anomalies.empty:
        cols = ["player_id", "match_type", "kills", "headshot_kills", "damage_dealt", "walk_distance", "anomaly_score", "warning_level", "reason"]
        print(anomalies[cols].to_string(index=False))

if __name__ == "__main__":
    main()
