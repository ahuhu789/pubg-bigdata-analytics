import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_spark_session
from src.feature_engineering import engineer_gameplay_features
from src.cassandra_client import CassandraClient
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)

class TestAnomalyDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = get_spark_session(app_name="UnitTest-Anomaly", master="local[1]", driver_memory="1g")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_feature_engineering_and_flags(self):
        schema = StructType([
            StructField("Id", StringType(), True),
            StructField("matchId", StringType(), True),
            StructField("groupId", StringType(), True),
            StructField("kills", IntegerType(), True),
            StructField("headshotKills", IntegerType(), True),
            StructField("damageDealt", DoubleType(), True),
            StructField("walkDistance", DoubleType(), True),
            StructField("rideDistance", DoubleType(), True),
            StructField("swimDistance", DoubleType(), True),
            StructField("longestKill", DoubleType(), True),
            StructField("matchDuration", IntegerType(), True),
            StructField("winPlacePerc", DoubleType(), True),
        ])

        test_data = [
            # Dòng 1: Người chơi thường
            ("norm1", "m1", "g1", 1, 0, 100.0, 1200.0, 0.0, 0.0, 50.0, 1400, 0.5),
            # Dòng 2: Nghi vấn dịch chuyển (kills=10, walkDistance=10.0m)
            ("tele1", "m1", "g2", 10, 1, 1000.0, 10.0, 0.0, 0.0, 20.0, 1400, 0.8),
            # Dòng 3: Nghi vấn aimbot (kills=12, headshots=12 => headshotRate=100%)
            ("aim1", "m1", "g3", 12, 12, 1200.0, 1500.0, 0.0, 0.0, 80.0, 1400, 1.0),
            # Dòng 4: Bắn xa siêu tưởng (longestKill = 1500m)
            ("range1", "m1", "g4", 5, 2, 500.0, 800.0, 0.0, 0.0, 1500.0, 1400, 0.6)
        ]

        df = self.spark.createDataFrame(test_data, schema)
        feat_df = engineer_gameplay_features(df)
        rows = {r.Id: r for r in feat_df.collect()}

        # Kiểm tra tính toán chia an toàn (không bị ZeroDivisionError)
        self.assertEqual(rows["norm1"].headshotRate, 0.0)
        self.assertEqual(rows["aim1"].headshotRate, 1.0)

        # Kiểm tra cờ phát hiện vi phạm luật chơi
        self.assertEqual(rows["tele1"].flag_teleport, 1)
        self.assertEqual(rows["aim1"].flag_aimbot, 1)
        self.assertEqual(rows["range1"].flag_extreme_range, 1)
        self.assertEqual(rows["norm1"].flag_teleport, 0)

    def test_cassandra_client_fallback_resilience(self):
        # CassandraClient must initialize safely even if Cassandra Docker is offline
        client = CassandraClient(host="127.0.0.1", port=9042)
        status = client.get_system_status()
        self.assertIn("active_storage", status)
        self.assertIn("message", status)

if __name__ == "__main__":
    unittest.main()
