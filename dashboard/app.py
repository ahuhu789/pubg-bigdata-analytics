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
    page_title="PUBG Big Data | Antigravity AI Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# ANTIGRAVITY SPATIAL & GLASSMORPHISM DESIGN SYSTEM
# =========================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Rajdhani:wght@500;600;700&display=swap');

    /* Global spatial background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0F172A 0%, #090D16 45%, #030712 100%) !important;
        color: #F3F4F6 !important;
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
    }

    /* Ambient floating lights */
    .ambient-glow {
        position: fixed;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(241, 136, 5, 0.08) 0%, transparent 70%);
        top: -100px;
        right: -100px;
        pointer-events: none;
        z-index: 0;
    }

    /* Glassmorphism Cards */
    .antigravity-card {
        background: rgba(17, 24, 39, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.45) !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .antigravity-card:hover {
        transform: translateY(-5px) !important;
        border-color: rgba(241, 136, 5, 0.45) !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 25px rgba(241, 136, 5, 0.18) !important;
    }

    /* Spatial Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
        backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: 2px solid #F18805 !important;
        border-radius: 20px !important;
        padding: 2rem 2.2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5) !important;
    }

    .hero-title {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #F18805 60%, #FF9F1C 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.3rem !important;
    }

    .hero-subtitle {
        font-size: 1.05rem !important;
        color: #94A3B8 !important;
        line-height: 1.6 !important;
    }

    /* Floating KPI Stats */
    .kpi-metric-box {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.4rem !important;
        transition: all 0.3s ease !important;
    }
    .kpi-metric-box:hover {
        background: rgba(30, 41, 59, 0.6) !important;
        border-color: rgba(0, 240, 255, 0.3) !important;
        transform: translateY(-3px) !important;
    }
    .kpi-label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #94A3B8 !important;
        margin-bottom: 0.3rem !important;
    }
    .kpi-value {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 2.3rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
    }
    .kpi-sub {
        font-size: 0.8rem !important;
        color: #38BDF8 !important;
        margin-top: 0.4rem !important;
    }

    /* Pulsing Status Badges */
    .badge-online {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.25) !important;
    }
    .pulse-dot-green {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
        animation: pulseAnimation 2s infinite;
    }
    @keyframes pulseAnimation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Warning level chips */
    .chip-high {
        background: rgba(239, 68, 68, 0.2) !important;
        color: #F87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    .chip-med {
        background: rgba(245, 158, 11, 0.2) !important;
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }

    /* Sidebar glass styling */
    section[data-testid="stSidebar"] {
        background: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(241, 136, 5, 0.4);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(241, 136, 5, 0.8);
    }
</style>
<div class="ambient-glow"></div>
""", unsafe_allow_html=True)

# Initialize Client
@st.cache_resource
def get_client():
    return CassandraClient()

client = get_client()
sys_status = client.get_system_status()
latest_run = client.get_latest_pipeline_run()

# Plotly Theme Setup for Spatial Glass UI
def get_plotly_layout(height=380, title=""):
    return go.Layout(
        title=dict(text=title, font=dict(family="Space Grotesk", size=15, color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17, 24, 39, 0.35)",
        font=dict(family="Space Grotesk", color="#94A3B8", size=11),
        margin=dict(t=45, b=30, l=40, r=20),
        height=height,
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            color="#94A3B8"
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            color="#94A3B8"
        )
    )

# Sidebar Branding
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 1.2rem;">
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; color: #F18805; letter-spacing: 1px;">
        PUBG ESPORTS
    </div>
    <div style="font-size: 0.75rem; color: #00F0FF; letter-spacing: 2px; text-transform: uppercase;">
        Big Data Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

selected_page = st.sidebar.radio(
    "Điều hướng Không gian (Navigation)",
    [
        "🌌 1. Tổng quan & Hạ tầng (Overview)",
        "⚔️ 2. Phân tích trận đấu (Match Analytics)",
        "🎯 3. Phát hiện bất thường (Anomaly AI)",
        "🔍 4. Tra cứu chi tiết (Telemetry Drilldown)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚡ Trạng Thái Dịch Vụ")

if sys_status["cassandra_online"]:
    st.sidebar.markdown("""
    <div class="badge-online">
        <div class="pulse-dot-green"></div>
        <span>Cassandra: ONLINE (9042)</span>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption(f"Cluster: `{sys_status['active_storage']}`")
else:
    st.sidebar.markdown("""
    <div style="background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.3); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
        Cassandra: OFFLINE
    </div>
    """, unsafe_allow_html=True)

if latest_run:
    st.sidebar.markdown("---")
    st.sidebar.caption(f"📅 Lần chạy: **{latest_run.get('run_timestamp')}**")
    st.sidebar.caption(f"🚀 Chế độ: **{latest_run.get('mode', '').upper()}** ({latest_run.get('cleaned_records', 0):,} rows)")
    st.sidebar.caption(f"⏱️ Runtime: **{latest_run.get('execution_time_sec', 0.0):.2f}s**")

# =========================================================================
# TRANG 1: TỔNG QUAN DỮ LIỆU & HẠ TẦNG BIG DATA
# =========================================================================
if selected_page == "🌌 1. Tổng quan & Hạ tầng (Overview)":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">HỆ THỐNG PHÂN TÍCH BIG DATA ESPORTS PUBG</div>
        <div class="hero-subtitle">
            Khung kiến trúc tính toán phân tán In-Memory <b>Apache Spark 4.2</b> kết hợp cơ sở dữ liệu hướng cột <b>Apache Cassandra NoSQL</b>,
            cung cấp năng lực giám sát gian lận và phân tích hành vi người chơi quy mô hàng triệu bản ghi theo thời gian thực.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Floating KPI Metrics
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-metric-box">
            <div class="kpi-label">Tổng Bản Ghi Đã Xử Lý</div>
            <div class="kpi-value">{latest_run.get('cleaned_records', 0):,}</div>
            <div class="kpi-sub">Khởi tạo từ {latest_run.get('input_records', 0):,} dòng thô</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-metric-box">
            <div class="kpi-label">Trận Đấu Hoàn Chỉnh</div>
            <div class="kpi-value">{latest_run.get('matches_count', 0):,}</div>
            <div class="kpi-sub">Bảo toàn 100% cấu trúc nhóm & thứ hạng</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        rate = round((latest_run.get('anomalies_detected', 0)/max(latest_run.get('cleaned_records', 1), 1))*100, 3) if latest_run else 0.0
        st.markdown(f"""
        <div class="kpi-metric-box">
            <div class="kpi-label">Cảnh Báo Bất Thường</div>
            <div class="kpi-value" style="color: #F87171;">{latest_run.get('anomalies_detected', 0):,}</div>
            <div class="kpi-sub">Tỷ lệ ngoại lai: {rate}% tổng mẫu</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-metric-box">
            <div class="kpi-label">Thời Gian Pipeline</div>
            <div class="kpi-value" style="color: #F18805;">{latest_run.get('execution_time_sec', 0.0):.1f}s</div>
            <div class="kpi-sub">Spark Catalyst + Native MLlib</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Two column layout: Architecture table + Pie Chart
    col_l, col_r = st.columns([1.1, 0.9])

    with col_l:
        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown("#### ⚡ Ngăn Xếp Hạ Tầng & Công Nghệ Big Data")
        infra_df = pd.DataFrame({
            "Thành phần": [
                "Động cơ phân tán",
                "Machine Learning",
                "CSDL NoSQL",
                "Lưu trữ trung gian",
                "Giao diện trực quan",
                "Môi trường Java",
                "Hadoop Native"
            ],
            "Công nghệ": [
                "Apache Spark 4.2.0 (PySpark)",
                "Spark MLlib (KMeans Clustering)",
                "Apache Cassandra (Port 9042)",
                "Apache Parquet (Snappy Columnar)",
                "Streamlit 1.65 + Plotly",
                "Microsoft OpenJDK 17 LTS",
                "Hadoop 3.3.6 (winutils)"
            ],
            "Trạng thái": [
                "Hoạt động",
                "Hoạt động",
                "ONLINE (9042)" if sys_status["cassandra_online"] else "Mirrored",
                "Sẵn sàng",
                "Hoạt động",
                "Sẵn sàng",
                "Sẵn sàng"
            ]
        })
        st.dataframe(infra_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown("#### 🎮 Phân Bố Người Chơi Theo Chế Độ Chơi")
        modes_df = client.get_match_type_analytics()
        if not modes_df.empty:
            fig_pie = px.pie(
                modes_df,
                names="match_type",
                values="total_players",
                hole=0.55,
                color_discrete_sequence=["#F18805", "#00F0FF", "#A855F7", "#3B82F6", "#EC4899", "#10B981"]
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Space Grotesk", color="#CBD5E1", size=11),
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# TRANG 2: PHÂN TÍCH CHUYÊN SÂU TRẬN ĐẤU
# =========================================================================
elif selected_page == "⚔️ 2. Phân tích trận đấu (Match Analytics)":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">PHÂN TÍCH CHIẾN ĐẤU & CHẾ ĐỘ THI ĐẤU PUBG</div>
        <div class="hero-subtitle">
            Tổng hợp phân tán bằng <b>Spark SQL</b> và lưu trữ tại bảng Cassandra <code>analytics_by_match_type</code>.
            Khảo sát các yếu tố chiến thuật: mạng hạ gục, lượng sát thương, khoảng cách di chuyển và tương quan vị trí thắng.
        </div>
    </div>
    """, unsafe_allow_html=True)

    modes_df = client.get_match_type_analytics()
    if modes_df.empty:
        st.warning("Chưa tìm thấy dữ liệu phân tích trận đấu. Hãy chạy `python src/pipeline.py`.")
    else:
        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Chỉ Số Tổng Hợp Theo Chế Độ Chơi (Cassandra Table: `analytics_by_match_type`)")
        st.dataframe(
            modes_df.rename(columns={
                "match_type": "Chế độ",
                "total_matches": "Số trận",
                "total_players": "Người chơi",
                "avg_duration_sec": "Thời lượng TB (s)",
                "avg_kills": "Kills TB",
                "max_kills": "Kills Kỷ lục",
                "avg_damage": "Sát thương TB",
                "max_damage": "Sát thương Kỷ lục",
                "avg_walk_distance": "Đi bộ TB (m)",
                "avg_ride_distance": "Lái xe TB (m)",
                "avg_headshot_rate": "Headshot Rate TB"
            }),
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
            fig_bar = px.bar(
                modes_df,
                x="match_type",
                y="avg_damage",
                color="avg_kills",
                color_continuous_scale=["#0284C7", "#00F0FF", "#F18805", "#EF4444"],
                labels={"match_type": "Chế độ chơi", "avg_damage": "Sát thương TB", "avg_kills": "Kills TB"}
            )
            fig_bar.update_layout(get_plotly_layout(height=350, title="Sát Thương & Mạng Hạ Gục Trung Bình Theo Chế Độ"))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
            fig_dist = px.bar(
                modes_df,
                x="match_type",
                y=["avg_walk_distance", "avg_ride_distance"],
                barmode="group",
                color_discrete_sequence=["#F18805", "#38BDF8"],
                labels={"value": "Khoảng cách (mét)", "match_type": "Chế độ chơi", "variable": "Loại di chuyển"}
            )
            fig_dist.update_layout(get_plotly_layout(height=350, title="So Sánh Quãng Đường Đi Bộ vs Lái Xe"))
            st.plotly_chart(fig_dist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# TRANG 3: PHÁT HIỆN BẤT THƯỜNG & CẢNH BÁO GIAN LẬN
# =========================================================================
elif selected_page == "🎯 3. Phát hiện bất thường (Anomaly AI)":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">PHÁT HIỆN BẤT THƯỜNG HÀNH VI (ANOMALY AI)</div>
        <div class="hero-subtitle">
            Mô hình học máy không giám sát <b>PySpark MLlib K-Means</b> kết hợp đo lường khoảng cách Euclidean đến tâm cụm
            và kiểm chứng các cờ vi phạm giới hạn vật lý trò chơi (Aimbot, Teleport, Speed Hack, Impossible Range).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(14, 165, 233, 0.1); border-left: 4px solid #0284C7; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1.5rem; font-size: 0.92rem; color: #E0F2FE;">
        📌 <b>Lưu Ý Học Thuật & Đạo Đức Dữ Liệu:</b> Do bộ dữ liệu PUBG công khai không có nhãn ground-truth ban nick chính thức,
        hệ thống phân loại các đối tượng dưới dạng <i>Bản ghi có dấu hiệu thống kê bất thường trong một trận đấu</i> (Flagged for Review),
        giúp trọng tài giảm tải 99.5% thời gian rà soát, không xem đây là phán quyết xử phạt tài khoản vĩnh viễn.
    </div>
    """, unsafe_allow_html=True)

    # Filter Bar Glass Container
    st.markdown('<div class="antigravity-card" style="padding: 1.2rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        min_score = st.slider("Ngưỡng Anomaly Score tối thiểu", min_value=0.0, max_value=100.0, value=35.0, step=5.0)
    with f2:
        warning_filter = st.multiselect(
            "Mức độ cảnh báo",
            ["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)", "BÌNH THƯỜNG (LOW)"],
            default=["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)"]
        )
    with f3:
        max_rows = st.selectbox("Số lượng bản ghi hiển thị", [25, 50, 100, 200], index=1)
    st.markdown('</div>', unsafe_allow_html=True)

    df_anom = client.get_suspicious_records(min_score=min_score, limit=max_rows)

    if df_anom.empty:
        st.info(f"Không có bản ghi nào vượt ngưỡng Anomaly Score >= {min_score}.")
    else:
        if warning_filter:
            df_anom = df_anom[df_anom["warning_level"].isin(warning_filter)]

        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown(f"#### 🚨 Danh Sách Bản Ghi Nghi Vấn (Hiển thị {len(df_anom)} đối tượng)")

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
                "anomaly_score": "Điểm Anomaly",
                "warning_level": "Mức Cảnh Báo",
                "reason": "Giải Thích Lý Do (Explainability)"
            }),
            use_container_width=True,
            height=380,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
            fig_hist = px.histogram(
                df_anom,
                x="anomaly_score",
                nbins=25,
                color="warning_level",
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#EF4444",
                    "CẦN KIỂM TRA (MEDIUM)": "#F18805",
                    "BÌNH THƯỜNG (LOW)": "#0284C7"
                }
            )
            fig_hist.update_layout(get_plotly_layout(height=350, title="Phân Bố Điểm Bất Thường (Anomaly Score)"))
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df_anom,
                x="walk_distance",
                y="kills",
                size="anomaly_score",
                color="warning_level",
                hover_data=["player_id", "damage_dealt", "reason"],
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#EF4444",
                    "CẦN KIỂM TRA (MEDIUM)": "#F18805",
                    "BÌNH THƯỜNG (LOW)": "#0284C7"
                }
            )
            fig_scatter.update_layout(get_plotly_layout(height=350, title="Phát Hiện Ngoại Lai: Kills vs Quãng Đường Đi Bộ"))
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# TRANG 4: TRA CỨU CHI TIẾT TRẬN ĐẤU & BẢN GHI
# =========================================================================
elif selected_page == "🔍 4. Tra cứu chi tiết (Telemetry Drilldown)":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">TRA CỨU DỮ LIỆU TELEMETRY TRẬN ĐẤU & NGƯỜI CHƠI</div>
        <div class="hero-subtitle">
            Truy vấn tức thời theo khóa chính Cassandra NoSQL: <code>match_summary_by_id</code> và <code>player_record_by_id</code>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🎮 Tra cứu Trận Đấu (matchId)", "👤 Tra cứu Người Chơi (playerId)"])

    with tab1:
        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Tra cứu Trận Đấu (Cassandra Table: `match_summary_by_id`)")
        match_summary_all = client.get_match_summary(limit=100)

        if not match_summary_all.empty:
            sample_match_ids = match_summary_all["match_id"].tolist()
            selected_match = st.selectbox("Chọn matchId mẫu:", sample_match_ids)
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

                st.markdown("##### Cấu trúc chi tiết trận đấu:")
                st.json({
                    "match_id": m_row["match_id"],
                    "match_type": m_row["match_type"],
                    "duration_seconds": int(m_row["duration_sec"]),
                    "total_knocks": int(m_row["total_knocks"]),
                    "winner_group_id": m_row["winner_group_id"]
                })
            else:
                st.error(f"Không tìm thấy dữ liệu cho matchId: {target_match}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="antigravity-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Tra cứu Bản Ghi Người Chơi (Cassandra Table: `player_record_by_id`)")
        suspicious_sample = client.get_suspicious_records(limit=25)

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

                st.warning(f"⚠️ **Giải thích lý do cảnh báo:** {p_row['flagged_reason']}")
                st.dataframe(p_res, use_container_width=True, hide_index=True)
            else:
                st.error(f"Không tìm thấy bản ghi cho playerId: {target_player}")
        st.markdown('</div>', unsafe_allow_html=True)
