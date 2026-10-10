import logging
from typing import Dict, Any, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnan

logger = logging.getLogger(__name__)

def clean_and_validate_data(df: DataFrame) -> Tuple[DataFrame, Dict[str, Any]]:
    """
    Cleans and validates the PUBG dataset using PySpark.
    
    Principles:
    - Drops corrupt rows (null primary keys or missing target winPlacePerc).
    - Preserves statistical extremes (high kills, huge damage) because these are
      crucial candidates for anomaly and fraud investigation.
    - Accurately tracks counts and data quality metrics.
    """
    raw_count = df.count()
    logger.info("Số bản ghi ban đầu: %d", raw_count)

    # 1. Kiểm tra giá trị Null trên các cột khóa và chỉ số quan trọng
    null_exprs = []
    for c in ["Id", "matchId", "groupId"]:
        null_exprs.append(count(when(col(c).isNull(), c)).alias(c))
    null_exprs.append(count(when(col("winPlacePerc").isNull() | isnan(col("winPlacePerc")), "winPlacePerc")).alias("winPlacePerc"))
    
    null_counts = df.select(null_exprs).collect()[0].asDict()

    logger.info("Thống kê giá trị Null: %s", null_counts)

    # 2. Loại bỏ các dòng bị lỗi cấu trúc: thiếu Id, matchId hoặc thiếu winPlacePerc
    cleaned_df = df.filter(
        col("Id").isNotNull() &
        col("matchId").isNotNull() &
        col("groupId").isNotNull() &
        col("winPlacePerc").isNotNull()
    )

    # 3. Lọc bỏ các dòng có giá trị hoàn toàn phi lý do lỗi truyền tải/cảm biến game
    # (Ví dụ khoảng cách âm hoặc thời lượng trận đấu âm).
    # Tuyệt đối KHÔNG loại bỏ chỉ số kill cao hoặc damage cao vì đó là mục tiêu phân tích bất thường.
    cleaned_df = cleaned_df.filter(
        (col("walkDistance") >= 0.0) &
        (col("rideDistance") >= 0.0) &
        (col("swimDistance") >= 0.0) &
        (col("kills") >= 0) &
        (col("damageDealt") >= 0.0) &
        (col("matchDuration") > 0)
    )

    cleaned_count = cleaned_df.count()
    dropped_count = raw_count - cleaned_count
    logger.info("Số bản ghi sau khi làm sạch: %d (Đã loại bỏ: %d)", cleaned_count, dropped_count)

    quality_report = {
        "raw_count": raw_count,
        "cleaned_count": cleaned_count,
        "dropped_count": dropped_count,
        "null_details": null_counts,
        "retention_rate": round((cleaned_count / raw_count) * 100, 4) if raw_count > 0 else 0.0
    }

    return cleaned_df, quality_report
