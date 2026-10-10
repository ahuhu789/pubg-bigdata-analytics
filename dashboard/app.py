import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.cassandra_client import CassandraClient

# Streamlit Page Configuration
st.set_page_config(
    page_title="PUBG Big Data Analytics & Anti-Cheat Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern esports styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F18805;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #A0AAB2;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E232A;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #F18805;
    }
    .status-badge-online {
        background-color: #0E7C47;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-badge-offline {
        background-color: #D9534F;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Cassandra / Storage Client
@st.cache_resource
def get_client():
    return CassandraClient()

client = get_client()
sys_status = client.get_system_status()
latest_run = client.get_latest_pipeline_run()

# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/PlayerUnknown%27s_Battlegrounds_Logo.svg", width=220)
st.sidebar.markdown("### 🏆 Môn: Nhập môn Big Data")
st.sidebar.markdown("**Đề tài:** Phân tích dữ liệu PUBG & Phát hiện người chơi có dấu hiệu bất thường")
st.sidebar.markdown("---")

selected_page = st.sidebar.radio(
    "Điều hướng Dashboard",
    [
        "📊 1. Tổng quan & Hạ tầng",
        "⚔️ 2. Phân tích trận đấu",
        "🎯 3. Phát hiện bất thường (Anomaly)",
        "🔍 4. Tra cứu chi tiết trận & Người chơi"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🖥️ Trạng thái Hệ thống")
if sys_status["cassandra_online"]:
    st.sidebar.markdown('<span class="status-badge-online">Cassandra: ONLINE (9042)</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="status-badge-offline">Cassandra: OFFLINE</span>', unsafe_allow_html=True)
    st.sidebar.caption("Đang dùng Local Persistent Cache (Cassandra Mirror)")

if latest_run:
    st.sidebar.caption(f"Lần chạy gần nhất: **{latest_run.get('run_timestamp')}**")
    st.sidebar.caption(f"Chế độ: **{latest_run.get('mode', '').upper()}** ({latest_run.get('cleaned_records', 0):,} bản ghi)")

# =========================================================================
# TRANG 1: TỔNG QUAN DỮ LIỆU & HẠ TẦNG BIG DATA
# =========================================================================
if selected_page == "📊 1. Tổng quan & Hạ tầng":
    st.markdown('<div class="main-header">📊 Tổng Quan Dữ Liệu & Hạ Tầng Big Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Kiến trúc kết hợp Apache Spark xử lý phân tán và Apache Cassandra lưu trữ truy vấn cao tốc</div>', unsafe_allow_html=True)

    if not sys_status["cassandra_online"]:
        st.warning(
            "⚠️ **Thông báo kết nối:** Dịch vụ Apache Cassandra (localhost:9042) hiện đang offline do máy cục bộ chưa bật Docker. "
            "Hệ thống đang tự động kích hoạt **Local Persistent Storage Mirror** với cấu trúc bảng và mô hình truy vấn tương đương 100% CQL Cassandra để Dashboard hiển thị dữ liệu liên tục."
        )

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="Tổng Bản Ghi Đã Xử Lý",
            value=f"{latest_run.get('cleaned_records', 0):,}" if latest_run else "0",
            delta=f"Khởi tạo từ {latest_run.get('input_records', 0):,}" if latest_run else None
        )
    with c2:
        st.metric(
            label="Số Trận Đấu Đánh Giá",
            value=f"{latest_run.get('matches_count', 0):,}" if latest_run else "0",
            delta="100% toàn vẹn nhóm"
        )
    with c3:
        st.metric(
            label="Dấu Hiệu Bất Thường Phát Hiện",
            value=f"{latest_run.get('anomalies_detected', 0):,}" if latest_run else "0",
            delta=f"{round((latest_run.get('anomalies_detected', 0)/max(latest_run.get('cleaned_records', 1), 1))*100, 2)}% tổng mẫu" if latest_run else None,
            delta_color="inverse"
        )
    with c4:
        st.metric(
            label="Thời Gian Thực Thi Pipeline",
            value=f"{latest_run.get('execution_time_sec', 0.0):.1f}s" if latest_run else "0s",
            delta="PySpark + MLlib"
        )

    st.markdown("---")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("⚙️ Thông Tin Hạ Tầng & Pipeline")
        infra_data = {
            "Thành phần": [
                "Công nghệ tính toán phân tán",
                "Động cơ học máy",
                "Hệ quản trị CSDL NoSQL",
                "Định dạng lưu trữ trung gian",
                "Khung giao diện Dashboard",
                "Môi trường thực thi Java",
                "Hadoop Native Binaries"
            ],
            "Phiên bản / Công nghệ": [
                "Apache Spark 4.2.0 (PySpark)",
                "Spark MLlib (KMeans Clustering)",
                "Apache Cassandra 4.1 / Local CQL Mirror",
                "Apache Parquet (Columnar Storage)",
                "Streamlit 1.65 + Plotly",
                "Microsoft OpenJDK 17.0.20",
                "Hadoop 3.3.6 (winutils.exe + hadoop.dll)"
            ],
            "Trạng thái": ["Hoạt động", "Hoạt động", sys_status["active_storage"], "Đã tạo", "Hoạt động", "Sẵn sàng", "Sẵn sàng"]
        }
        st.table(pd.DataFrame(infra_data))

    with col_right:
        st.subheader("📈 Phân Bố Người Chơi Theo Chế Độ Chơi")
        modes_df = client.get_match_type_analytics()
        if not modes_df.empty:
            fig_pie = px.pie(
                modes_df,
                names="match_type",
                values="total_players",
                color_discrete_sequence=px.colors.qualitative.Bold,
                hole=0.4
            )
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu thống kê chế độ chơi. Vui lòng chạy pipeline trước.")

# =========================================================================
# TRANG 2: PHÂN TÍCH CHUYÊN SÂU TRẬN ĐẤU
# =========================================================================
elif selected_page == "⚔️ 2. Phân tích trận đấu":
    st.markdown('<div class="main-header">⚔️ Phân Tích Thống Kê Trận Đấu PUBG</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Phân tích mối quan hệ giữa các chỉ số thi đấu, khoảng cách di chuyển và tỷ lệ thắng</div>', unsafe_allow_html=True)

    modes_df = client.get_match_type_analytics()
    if modes_df.empty:
        st.warning("Chưa có dữ liệu phân tích trận đấu trong Cassandra. Hãy chạy `python src/pipeline.py`.")
    else:
        st.subheader("📋 Bảng Tổng Hợp Chỉ Số Theo Chế Độ Chơi (Cassandra Table: `analytics_by_match_type`)")
        st.dataframe(
            modes_df.rename(columns={
                "match_type": "Chế độ",
                "total_matches": "Số trận",
                "total_players": "Số người chơi",
                "avg_duration_sec": "Thời lượng TB (s)",
                "avg_kills": "Kills TB",
                "max_kills": "Kills Kỷ lục",
                "avg_damage": "Sát thương TB",
                "max_damage": "Sát thương Kỷ lục",
                "avg_walk_distance": "Đi bộ TB (m)",
                "avg_ride_distance": "Lái xe TB (m)",
                "avg_headshot_rate": "Headshot Rate TB"
            }),
            use_container_width=True
        )

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("🎯 So Sánh Sát Thương & Mạng Hạ Gục TB")
            fig_bar = px.bar(
                modes_df,
                x="match_type",
                y="avg_damage",
                color="avg_kills",
                labels={"match_type": "Chế độ chơi", "avg_damage": "Sát thương TB", "avg_kills": "Kills TB"},
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(height=380)
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.subheader("🏃 Quãng Đường Di Chuyển Trung Bình")
            fig_dist = px.bar(
                modes_df,
                x="match_type",
                y=["avg_walk_distance", "avg_ride_distance"],
                barmode="group",
                labels={"value": "Khoảng cách (m)", "match_type": "Chế độ chơi", "variable": "Loại di chuyển"}
            )
            fig_dist.update_layout(height=380)
            st.plotly_chart(fig_dist, use_container_width=True)

# =========================================================================
# TRANG 3: PHÁT HIỆN BẤT THƯỜNG & CẢNH BÁO GIAN LẬN
# =========================================================================
elif selected_page == "🎯 3. Phát hiện bất thường (Anomaly)":
    st.markdown('<div class="main-header">🎯 Phát Hiện Bản Ghi Có Dấu Hiệu Bất Thường</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Mô hình phân cụm không giám sát PySpark MLlib KMeans kết hợp cờ vi phạm vật lý thi đấu</div>', unsafe_allow_html=True)

    st.info(
        "📌 **Lưu ý học thuật & Đạo đức dữ liệu:** Do bộ dữ liệu công khai PUBG không có nhãn gian lận được xác minh (Ground Truth), "
        "bài toán được thiết kế chuẩn xác dưới dạng **Phát hiện bất thường thống kê (Unsupervised Anomaly Detection)**. "
        "Các đối tượng được đánh dấu đại diện cho bản ghi người chơi-trận đấu có chỉ số chênh lệch cực đoan cần xem xét (Flagged for Review), "
        "không xem đây là kết luận xử phạt tài khoản."
    )

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        min_score = st.slider("Ngưỡng Anomaly Score tối thiểu", min_value=0.0, max_value=100.0, value=35.0, step=5.0)
    with col_f2:
        warning_filter = st.multiselect(
            "Mức độ cảnh báo",
            ["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)", "BÌNH THƯỜNG (LOW)"],
            default=["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)"]
        )
    with col_f3:
        max_rows = st.selectbox("Số lượng hiển thị", [20, 50, 100, 200], index=1)

    df_anom = client.get_suspicious_records(min_score=min_score, limit=max_rows)

    if df_anom.empty:
        st.warning(f"Không có bản ghi nào có Anomaly Score >= {min_score}.")
    else:
        if warning_filter:
            df_anom = df_anom[df_anom["warning_level"].isin(warning_filter)]

        st.subheader(f"🚨 Danh Sách Đối Tượng Nghi Vấn (Hiển thị {len(df_anom)} bản ghi)")

        # Display Interactive Table
        display_cols = [
            "player_id", "match_type", "kills", "headshot_kills",
            "damage_dealt", "walk_distance", "anomaly_score", "warning_level", "reason"
        ]
        st.dataframe(
            df_anom[display_cols].rename(columns={
                "player_id": "Mã Người Chơi (Id)",
                "match_type": "Chế độ",
                "kills": "Kills",
                "headshot_kills": "Headshots",
                "damage_dealt": "Sát thương",
                "walk_distance": "Đi bộ (m)",
                "anomaly_score": "Điểm Bất Thường",
                "warning_level": "Mức Cảnh Báo",
                "reason": "Giải Thích Lý Do (Explainability)"
            }),
            use_container_width=True,
            height=400
        )

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📊 Phân Bố Điểm Bất Thường (Anomaly Score)")
            fig_hist = px.histogram(
                df_anom,
                x="anomaly_score",
                nbins=20,
                color="warning_level",
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#D9534F",
                    "CẦN KIỂM TRA (MEDIUM)": "#F18805",
                    "BÌNH THƯỜNG (LOW)": "#5BC0DE"
                },
                labels={"anomaly_score": "Anomaly Score"}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with c2:
            st.subheader("🎯 Tương Quan: Kills vs Quãng Đường Đi Bộ")
            fig_scatter = px.scatter(
                df_anom,
                x="walk_distance",
                y="kills",
                size="anomaly_score",
                color="warning_level",
                hover_data=["player_id", "damage_dealt", "reason"],
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#D9534F",
                    "CẦN KIỂM TRA (MEDIUM)": "#F18805",
                    "BÌNH THƯỜNG (LOW)": "#5BC0DE"
                },
                labels={"walk_distance": "Khoảng cách đi bộ (m)", "kills": "Số mạng hạ gục"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

# =========================================================================
# TRANG 4: TRA CỨU CHI TIẾT TRẬN ĐẤU & BẢN GHI
# =========================================================================
elif selected_page == "🔍 4. Tra cứu chi tiết trận & Người chơi":
    st.markdown('<div class="main-header">🔍 Tra Cứu Chi Tiết Bản Ghi & Trận Đấu</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Truy vấn chi tiết từng trận đấu hoặc hồ sơ người chơi theo khóa chính CQL</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🎮 Tra cứu Trận Đấu (matchId)", "👤 Tra cứu Bản Ghi Người Chơi (playerId)"])

    with tab1:
        st.subheader("Tra cứu thông tin trận đấu (Table: `match_summary_by_id`)")
        match_summary_all = client.get_match_summary(limit=100)
        
        if not match_summary_all.empty:
            sample_match_ids = match_summary_all["match_id"].tolist()
            selected_match = st.selectbox("Chọn matchId mẫu từ Cassandra hoặc nhập bên dưới:", sample_match_ids)
            custom_match = st.text_input("Hoặc nhập chính xác matchId:", value=selected_match)
            
            target_match = custom_match.strip() if custom_match.strip() else selected_match
            match_res = client.get_match_summary(match_id=target_match)
            
            if not match_res.empty:
                m_row = match_res.iloc[0]
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Chế độ chơi", m_row["match_type"])
                m2.metric("Số người tham gia", f"{m_row['num_players']}")
                m3.metric("Kills cao nhất trong trận", f"{m_row['max_kills']}")
                m4.metric("Sát thương top 1", f"{m_row['top_damage']:.1f}")
                
                st.markdown("#### Chi tiết cấu trúc trận đấu:")
                st.json({
                    "match_id": m_row["match_id"],
                    "match_type": m_row["match_type"],
                    "duration_seconds": int(m_row["duration_sec"]),
                    "total_knocks": int(m_row["total_knocks"]),
                    "winner_group_id": m_row["winner_group_id"]
                })
            else:
                st.error(f"Không tìm thấy dữ liệu cho matchId: {target_match}")
        else:
            st.info("Chưa có dữ liệu trận đấu. Hãy chạy pipeline trước.")

    with tab2:
        st.subheader("Tra cứu bản ghi người chơi (Table: `player_record_by_id`)")
        suspicious_sample = client.get_suspicious_records(limit=20)
        
        if not suspicious_sample.empty:
            sample_player_ids = suspicious_sample["player_id"].tolist()
            selected_player = st.selectbox("Chọn playerId nghi vấn mẫu:", sample_player_ids)
            custom_player = st.text_input("Hoặc nhập chính xác playerId:", value=selected_player)
            
            target_player = custom_player.strip() if custom_player.strip() else selected_player
            p_res = client.get_player_records(player_id=target_player)
            
            if not p_res.empty:
                p_row = p_res.iloc[0]
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Số Kills", f"{p_row['kills']}")
                c2.metric("Headshots", f"{p_row['headshot_kills']}")
                c3.metric("Sát thương", f"{p_row['damage_dealt']:.1f}")
                c4.metric("Điểm Bất Thường", f"{p_row['anomaly_score']:.1f}")

                st.warning(f"⚠️ **Nguyên nhân bị cảnh báo:** {p_row['flagged_reason']}")
                st.table(p_res)
            else:
                st.error(f"Không tìm thấy bản ghi cho playerId: {target_player}")
        else:
            st.info("Chưa có danh sách người chơi bất thường. Hãy chạy pipeline trước.")
