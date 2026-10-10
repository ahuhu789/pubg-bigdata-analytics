import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_spark_session
from src.preprocessing import clean_and_validate_data
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)

class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = get_spark_session(app_name="UnitTest-Preprocessing", master="local[1]", driver_memory="1g")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_null_handling_and_extreme_preservation(self):
        schema = StructType([
            StructField("Id", StringType(), True),
            StructField("groupId", StringType(), True),
            StructField("matchId", StringType(), True),
            StructField("kills", IntegerType(), True),
            StructField("damageDealt", DoubleType(), True),
            StructField("walkDistance", DoubleType(), True),
            StructField("rideDistance", DoubleType(), True),
            StructField("swimDistance", DoubleType(), True),
            StructField("matchDuration", IntegerType(), True),
            StructField("winPlacePerc", DoubleType(), True),
        ])

        test_data = [
            # Dòng 1: Hợp lệ bình thường
            ("p1", "g1", "m1", 2, 200.0, 1500.0, 0.0, 0.0, 1400, 0.5),
            # Dòng 2: Thiếu winPlacePerc (cần bị loại bỏ)
            ("p2", "g1", "m1", 1, 100.0, 500.0, 0.0, 0.0, 1400, None),
            # Dòng 3: Thiếu matchId (cần bị loại bỏ)
            ("p3", "g2", None, 0, 0.0, 100.0, 0.0, 0.0, 1400, 0.1),
            # Dòng 4: Cực trị (50 kills, 5000 damage) - PHẢI ĐƯỢC GIỮ LẠI ĐỂ PHÂN TÍCH GIAN LẬN
            ("p4", "g3", "m1", 50, 5000.0, 2000.0, 0.0, 0.0, 1400, 1.0),
            # Dòng 5: Giá trị âm phi lý do lỗi cảm biến game (cần bị loại bỏ)
            ("p5", "g4", "m1", 1, 100.0, -50.0, 0.0, 0.0, 1400, 0.3)
        ]

        raw_df = self.spark.createDataFrame(test_data, schema)
        cleaned_df, report = clean_and_validate_data(raw_df)

        # Kiểm tra số lượng
        self.assertEqual(report["raw_count"], 5)
        self.assertEqual(report["cleaned_count"], 2) # Chỉ p1 và p4 thỏa mãn
        
        # Kiểm tra chắc chắn dòng cực trị p4 được giữ lại
        retained_ids = [row.Id for row in cleaned_df.collect()]
        self.assertIn("p4", retained_ids)
        self.assertIn("p1", retained_ids)
        self.assertNotIn("p2", retained_ids)
        self.assertNotIn("p3", retained_ids)
        self.assertNotIn("p5", retained_ids)

if __name__ == "__main__":
    unittest.main()
