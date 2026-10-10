import logging
from typing import Dict, Any, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, count, countDistinct, avg, max, min, sum, round as spark_round,
    when, corr
)

logger = logging.getLogger(__name__)

def compute_match_type_analytics(df: DataFrame) -> DataFrame:
    """
    Computes statistical aggregations per game mode (matchType).
    Directly answers: Which modes have the most matches, players, and average duration?
    """
    logger.info("Đang tổng hợp số liệu theo chế độ chơi (matchType)...")
    
    # Calculate total distance and safe headshot rate
    stats_df = (
        df.groupBy("matchType")
        .agg(
            countDistinct("matchId").alias("total_matches"),
            count("Id").alias("total_players"),
            spark_round(avg("matchDuration"), 2).alias("avg_duration_sec"),
            spark_round(avg("kills"), 2).alias("avg_kills"),
            max("kills").alias("max_kills"),
            spark_round(avg("damageDealt"), 2).alias("avg_damage"),
            spark_round(max("damageDealt"), 2).alias("max_damage"),
            spark_round(avg("walkDistance"), 2).alias("avg_walk_distance"),
            spark_round(avg("rideDistance"), 2).alias("avg_ride_distance"),
            spark_round(avg(when(col("kills") > 0, col("headshotKills") / col("kills")).otherwise(0.0)), 4).alias("avg_headshot_rate")
        )
        .orderBy(col("total_players").desc())
    )
    
    return stats_df

def compute_match_summary(df: DataFrame) -> DataFrame:
    """
    Computes match-level summaries and identifiers for drill-down.
    """
    logger.info("Đang tổng hợp thông tin cấp độ trận đấu (matchId)...")
    
    match_df = (
        df.groupBy("matchId", "matchType")
        .agg(
            count("Id").alias("num_players"),
            max("matchDuration").alias("duration_sec"),
            max("kills").alias("max_kills"),
            spark_round(max("damageDealt"), 2).alias("top_damage"),
            sum("DBNOs").alias("total_knocks"),
            max(when(col("winPlacePerc") == 1.0, col("groupId")).otherwise(None)).alias("winner_group_id")
        )
    )
    
    return match_df

def compute_combat_correlations(df: DataFrame) -> Dict[str, float]:
    """
    Computes Pearson correlation coefficients of combat and survival metrics with winPlacePerc.
    Directly answers: How do kills, damage, and movement correlate with match victory?
    """
    logger.info("Đang tính toán hệ số tương quan với winPlacePerc...")
    metrics = ["kills", "damageDealt", "headshotKills", "killStreaks", "walkDistance", "boosts", "heals", "weaponsAcquired"]
    
    correlations = {}
    for m in metrics:
        corr_val = df.stat.corr(m, "winPlacePerc")
        correlations[f"corr_{m}_winPlace"] = round(float(corr_val), 4) if corr_val is not None else 0.0
        
    return correlations
