-- =========================================================================
-- Apache Cassandra Schema for PUBG Big Data Analytics & Anomaly Detection
-- Keyspace: pubg_analytics
-- =========================================================================

CREATE KEYSPACE IF NOT EXISTS pubg_analytics
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE pubg_analytics;

-- 1. Table: Analytics summarized by Match Type (e.g. squad-fpp, duo, solo-fpp)
-- Optimized for Page 2: Match Analytics filter & comparison
CREATE TABLE IF NOT EXISTS analytics_by_match_type (
    match_type text,
    total_matches bigint,
    total_players bigint,
    avg_duration_sec double,
    avg_kills double,
    max_kills int,
    avg_damage double,
    max_damage double,
    avg_walk_distance double,
    avg_ride_distance double,
    avg_headshot_rate double,
    PRIMARY KEY (match_type)
);

-- 2. Table: Match-level aggregated summary
-- Optimized for Page 4: Match detail drill-down
CREATE TABLE IF NOT EXISTS match_summary_by_id (
    match_id text,
    match_type text,
    num_players int,
    duration_sec int,
    max_kills int,
    top_damage double,
    total_knocks int,
    anomalous_records_count int,
    winner_group_id text,
    PRIMARY KEY (match_id)
);

-- 3. Table: Suspicious player-match records by pipeline run
-- Partitioned by run_id, sorted descending by anomaly_score for efficient pagination
-- Follows Cassandra best practice: NO ALLOW FILTERING needed for top-N ranking
CREATE TABLE IF NOT EXISTS suspicious_records_by_run (
    run_id text,
    anomaly_score double,
    player_id text,
    match_id text,
    match_type text,
    kills int,
    headshot_kills int,
    damage_dealt double,
    longest_kill double,
    walk_distance double,
    total_distance double,
    cluster_id int,
    warning_level text,
    reason text,
    PRIMARY KEY (run_id, anomaly_score, player_id)
) WITH CLUSTERING ORDER BY (anomaly_score DESC, player_id ASC);

-- 4. Table: Individual player-match records lookup
-- Lookup by player_id across matchId
CREATE TABLE IF NOT EXISTS player_record_by_id (
    player_id text,
    match_id text,
    group_id text,
    match_type text,
    kills int,
    damage_dealt double,
    headshot_kills int,
    walk_distance double,
    total_distance double,
    win_place_perc double,
    anomaly_score double,
    is_anomalous boolean,
    flagged_reason text,
    PRIMARY KEY (player_id, match_id)
);

-- 5. Table: Pipeline execution metadata and health stats
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id text,
    mode text,
    input_records bigint,
    cleaned_records bigint,
    matches_count int,
    anomalies_detected int,
    execution_time_sec double,
    run_timestamp timestamp,
    status text,
    PRIMARY KEY (run_id)
);
