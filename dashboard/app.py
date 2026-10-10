import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Thiết lập đường dẫn thư mục gốc
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.cassandra_client import CassandraClient

# Cấu hình trang Streamlit chuẩn học thuật & doanh nghiệp
st.set_page_config(
    page_title="Hệ Thống Phân Tích Dữ Liệu PUBG & Phát Hiện Bất Thường",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# PHONG CÁCH THIẾT KẾ PHẲNG CHUYÊN NGHIỆP (CLEAN & FLAT ENTERPRISE THEME)
# =========================================================================
st.markdown("""
<style>
    /* Tổng thể giao diện sáng, tối giản và dễ đọc */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Khối tiêu đề chính */
    .header-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 24px 28px !important;
        margin-bottom: 20px !important;
    }
    .header-title {
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 6px !important;
        letter-spacing: -0.3px !important;
    }
    .header-desc {
        font-size: 0.95rem !important;
        color: #475569 !important;
        line-height: 1.55 !important;
    }

    /* Thẻ chỉ số đo lường (KPI Metric Box) */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        margin-bottom: 12px !important;
    }
    .metric-label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #64748B !important;
        margin-bottom: 4px !important;
    }
    .metric-val {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        line-height: 1.2 !important;
    }
    .metric-caption {
        font-size: 0.8rem !important;
        color: #64748B !important;
        margin-top: 4px !important;
    }

    /* Khối chứa nội dung biểu đồ và bảng dữ liệu */
    .content-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 20px 24px !important;
        margin-bottom: 18px !important;
    }
    .content-box-title {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #1E293B !important;
        margin-bottom: 14px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        padding-bottom: 8px !important;
    }

    /* Thanh điều hướng Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Huy hiệu trạng thái tối giản */
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge-ok {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #BBF7D0;
    }
    .status-badge-err {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }

    /* Tinh chỉnh bảng dữ liệu Streamlit */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo kết nối CSDL Cassandra Client
@st.cache_resource
def get_client():
    return CassandraClient()

client = get_client()
sys_status = client.get_system_status()
latest_run = client.get_latest_pipeline_run()

# Cấu hình hàm định dạng Plotly chuẩn hiển thị học thuật
def get_clean_plotly_layout(title="", height=360):
    return go.Layout(
        title=dict(
            text=title,
            font=dict(size=14, color="#1E293B", family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto")
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        template="plotly_white",
        font=dict(color="#475569", size=11),
        margin=dict(t=45, b=35, l=45, r=20),
        height=height,
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            linecolor="#CBD5E1",
            tickcolor="#CBD5E1"
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            linecolor="#CBD5E1",
            tickcolor="#CBD5E1"
        )
    )

# Sidebar: Thông tin hệ thống và điều hướng
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 14px;">
    <div style="font-size: 1.15rem; font-weight: 700; color: #0F172A; line-height: 1.3;">
        PUBG Big Data Analytics
    </div>
    <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
        Đồ Án Môn Học Nhập Môn Big Data
    </div>
</div>
""", unsafe_allow_html=True)

selected_page = st.sidebar.radio(
    "Danh mục quản trị",
    [
        "1. Tổng quan hệ thống",
        "2. Phân tích thống kê trận đấu",
        "3. Phát hiện hành vi bất thường",
        "4. Tra cứu chi tiết telemetry"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Trạng Thái Dịch Vụ**")

if sys_status["cassandra_online"]:
    st.sidebar.markdown("""
    <div class="status-badge status-badge-ok">
        Apache Cassandra: Đang hoạt động (9042)
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption(f"Keyspace: `{sys_status['active_storage']}`")
else:
    st.sidebar.markdown("""
    <div class="status-badge status-badge-err">
        Apache Cassandra: Không kết nối
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption(f"Lưu trữ cục bộ: `{sys_status['active_storage']}`")

if latest_run:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Thông Tin Pipeline**")
    st.sidebar.caption(f"Thời gian chạy: **{latest_run.get('run_timestamp')}**")
    st.sidebar.caption(f"Chế độ: **{latest_run.get('mode', '').upper()}** ({latest_run.get('cleaned_records', 0):,} dòng)")
    st.sidebar.caption(f"Thời gian thực thi: **{latest_run.get('execution_time_sec', 0.0):.2f} giây**")

# =========================================================================
# TRANG 1: TỔNG QUAN HỆ THỐNG
# =========================================================================
if selected_page == "1. Tổng quan hệ thống":
    st.markdown("""
    <div class="header-box">
        <div class="header-title">Hệ Thống Phân Tích Dữ Liệu PUBG & Giám Sát Hành Vi Bất Thường</div>
        <div class="header-desc">
            Kiến trúc xử lý dữ liệu lớn kết hợp tính toán phân tán In-Memory <b>Apache Spark</b> và cơ sở dữ liệu phân tán NoSQL <b>Apache Cassandra</b>. 
            Hệ thống cung cấp năng lực tổng hợp thống kê hiệu suất thi đấu và phát hiện các mẫu hành vi vi phạm vật lý trò chơi trên quy mô lớn.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hiển thị các chỉ số đo lường chính (KPI Cards)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Bản Ghi Đã Xử Lý</div>
            <div class="metric-val">{latest_run.get('cleaned_records', 0):,}</div>
            <div class="metric-caption">Từ {latest_run.get('input_records', 0):,} dòng dữ liệu thô</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Trận Đấu Hoàn Chỉnh</div>
            <div class="metric-val">{latest_run.get('matches_count', 0):,}</div>
            <div class="metric-caption">Bảo toàn cấu trúc đội và thứ hạng</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        rate = round((latest_run.get('anomalies_detected', 0)/max(latest_run.get('cleaned_records', 1), 1))*100, 3) if latest_run else 0.0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Bản Ghi Nghi Vấn</div>
            <div class="metric-val" style="color: #DC2626;">{latest_run.get('anomalies_detected', 0):,}</div>
            <div class="metric-caption">Tỷ lệ ngoại lai: {rate}% tổng mẫu</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Thời Gian Thực Thi</div>
            <div class="metric-val" style="color: #2563EB;">{latest_run.get('execution_time_sec', 0.0):.1f}s</div>
            <div class="metric-caption">Động cơ Spark SQL + Spark MLlib</div>
        </div>
        """, unsafe_allow_html=True)

    c_left, c_right = st.columns([1.1, 0.9])

    with c_left:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">Ngăn Xếp Hạ Tầng & Thành Phần Kỹ Thuật</div>
        </div>
        """, unsafe_allow_html=True)
        infra_df = pd.DataFrame({
            "Thành phần": [
                "Động cơ phân tán",
                "Machine Learning",
                "Cơ sở dữ liệu",
                "Định dạng trung gian",
                "Giao diện trực quan",
                "Môi trường Java",
                "Native Winutils"
            ],
            "Công nghệ sử dụng": [
                "Apache Spark 4.2.0 (PySpark)",
                "Spark MLlib (K-Means Clustering)",
                "Apache Cassandra (Cổng 9042)",
                "Apache Parquet (Snappy Columnar)",
                "Streamlit 1.65 + Plotly",
                "Microsoft OpenJDK 17 LTS",
                "Hadoop 3.3.6 winutils.exe"
            ],
            "Trạng thái vận hành": [
                "Sẵn sàng",
                "Sẵn sàng",
                "Hoạt động (9042)" if sys_status["cassandra_online"] else "Đồng bộ tệp cục bộ",
                "Sẵn sàng",
                "Hoạt động",
                "Sẵn sàng",
                "Sẵn sàng"
            ]
        })
        st.dataframe(infra_df, use_container_width=True, hide_index=True)

    with c_right:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">Phân Bố Người Chơi Theo Chế Độ Chơi</div>
        </div>
        """, unsafe_allow_html=True)
        modes_df = client.get_match_type_analytics()
        if not modes_df.empty:
            fig_pie = px.pie(
                modes_df,
                names="match_type",
                values="total_players",
                hole=0.45,
                color_discrete_sequence=["#2563EB", "#0D9488", "#D97706", "#64748B", "#DC2626", "#0284C7"]
            )
            fig_pie.update_layout(
                paper_bgcolor="#FFFFFF",
                font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto", color="#475569", size=11),
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# =========================================================================
# TRANG 2: PHÂN TÍCH THỐNG KÊ TRẬN ĐẤU
# =========================================================================
elif selected_page == "2. Phân tích thống kê trận đấu":
    st.markdown("""
    <div class="header-box">
        <div class="header-title">Phân Tích Thống Kê Trận Đấu & Hiệu Suất Chiến Đấu</div>
        <div class="header-desc">
            Dữ liệu được tổng hợp song song bằng <b>PySpark DataFrame</b> và truy vấn trực tiếp từ bảng Cassandra <code>analytics_by_match_type</code>.
            Trang này phân tích các khía cạnh tương quan: lượng sát thương, số mạng hạ gục, thời lượng thi đấu và quãng đường di chuyển.
        </div>
    </div>
    """, unsafe_allow_html=True)

    modes_df = client.get_match_type_analytics()
    if modes_df.empty:
        st.warning("Chưa tìm thấy dữ liệu thống kê. Vui lòng chạy pipeline bằng lệnh: `python src/pipeline.py`.")
    else:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">Bảng Tổng Hợp Chỉ Số Theo Chế Độ Chơi (Bảng Cassandra: analytics_by_match_type)</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            modes_df.rename(columns={
                "match_type": "Chế độ",
                "total_matches": "Số trận",
                "total_players": "Số người chơi",
                "avg_duration_sec": "Thời lượng TB (s)",
                "avg_kills": "Hạ gục TB",
                "max_kills": "Hạ gục Kỷ lục",
                "avg_damage": "Sát thương TB",
                "max_damage": "Sát thương Kỷ lục",
                "avg_walk_distance": "Đi bộ TB (m)",
                "avg_ride_distance": "Lái xe TB (m)",
                "avg_headshot_rate": "Tỷ lệ Headshot TB"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        g1, g2 = st.columns(2)
        with g1:
            st.markdown("""
            <div class="content-box">
                <div class="content-box-title">Sát Thương Trung Bình & Số Mạng Hạ Gục Theo Chế Độ</div>
            </div>
            """, unsafe_allow_html=True)
            fig_bar = px.bar(
                modes_df,
                x="match_type",
                y="avg_damage",
                color="avg_kills",
                color_continuous_scale=["#93C5FD", "#2563EB", "#1E3A8A"],
                labels={"match_type": "Chế độ chơi", "avg_damage": "Sát thương trung bình", "avg_kills": "Hạ gục TB"}
            )
            fig_bar.update_layout(get_clean_plotly_layout(height=340))
            st.plotly_chart(fig_bar, use_container_width=True)

        with g2:
            st.markdown("""
            <div class="content-box">
                <div class="content-box-title">So Sánh Quãng Đường Đi Bộ & Đi Xe Theo Chế Độ</div>
            </div>
            """, unsafe_allow_html=True)
            fig_dist = px.bar(
                modes_df,
                x="match_type",
                y=["avg_walk_distance", "avg_ride_distance"],
                barmode="group",
                color_discrete_sequence=["#2563EB", "#0D9488"],
                labels={"value": "Khoảng cách (mét)", "match_type": "Chế độ chơi", "variable": "Loại di chuyển"}
            )
            fig_dist.update_layout(get_clean_plotly_layout(height=340))
            st.plotly_chart(fig_dist, use_container_width=True)

# =========================================================================
# TRANG 3: PHÁT HIỆN HÀNH VI BẤT THƯỜNG
# =========================================================================
elif selected_page == "3. Phát hiện hành vi bất thường":
    st.markdown("""
    <div class="header-box">
        <div class="header-title">Mô Hình Phát Hiện Bất Thường & Sàng Lọc Gian Lận</div>
        <div class="header-desc">
            Ứng dụng thuật toán phân cụm không giám sát <b>Spark MLlib K-Means</b> kết hợp tính toán khoảng cách Euclidean đến trọng tâm cụm 
            và kiểm tra các luật giới hạn vật lý trò chơi (Aimbot, Teleport, Speed Hack, Impossible Range).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "**Lưu ý học thuật & Đạo đức dữ liệu:** Bộ dữ liệu PUBG công khai không cung cấp nhãn cấm chính thức (Ground-truth Bans). "
        "Do đó, bài toán được định nghĩa chính xác là **Phát hiện ngoại lai thống kê theo từng bản ghi trận đấu** nhằm mục đích hỗ trợ đội ngũ trọng tài "
        "thu hẹp phạm vi kiểm tra thủ công từ hàng triệu bản ghi xuống dưới 1% trường hợp có xác suất bất thường cao nhất."
    )

    # Bộ lọc điều kiện
    st.markdown("""
    <div class="content-box">
        <div class="content-box-title">Bộ Lọc Tham Số Phát Hiện</div>
    </div>
    """, unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        min_score = st.slider("Điểm bất thường tối thiểu (Anomaly Score)", min_value=0.0, max_value=100.0, value=35.0, step=5.0)
    with f2:
        warning_filter = st.multiselect(
            "Mức độ cảnh báo",
            ["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)", "BÌNH THƯỜNG (LOW)"],
            default=["NGUY CƠ CAO (HIGH)", "CẦN KIỂM TRA (MEDIUM)"]
        )
    with f3:
        max_rows = st.selectbox("Số lượng bản ghi tối đa", [25, 50, 100, 200], index=1)

    df_anom = client.get_suspicious_records(min_score=min_score, limit=max_rows)

    if df_anom.empty:
        st.warning(f"Không có bản ghi nào đáp ứng ngưỡng Anomaly Score >= {min_score}.")
    else:
        if warning_filter:
            df_anom = df_anom[df_anom["warning_level"].isin(warning_filter)]

        st.markdown(f"""
        <div class="content-box">
            <div class="content-box-title">Danh Sách Bản Ghi Bị Đánh Dấu Cần Kiểm Tra (Tổng số: {len(df_anom)})</div>
        </div>
        """, unsafe_allow_html=True)

        display_cols = [
            "player_id", "match_type", "kills", "headshot_kills",
            "damage_dealt", "walk_distance", "anomaly_score", "warning_level", "reason"
        ]
        st.dataframe(
            df_anom[display_cols].rename(columns={
                "player_id": "Mã Người Chơi",
                "match_type": "Chế độ",
                "kills": "Hạ gục",
                "headshot_kills": "Headshots",
                "damage_dealt": "Sát thương",
                "walk_distance": "Đi bộ (m)",
                "anomaly_score": "Điểm Bất Thường",
                "warning_level": "Mức Cảnh Báo",
                "reason": "Giải Thích Lý Do Cảnh Báo"
            }),
            use_container_width=True,
            height=360,
            hide_index=True
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("""
            <div class="content-box">
                <div class="content-box-title">Phân Bố Tần Suất Điểm Bất Thường (Anomaly Score)</div>
            </div>
            """, unsafe_allow_html=True)
            fig_hist = px.histogram(
                df_anom,
                x="anomaly_score",
                nbins=25,
                color="warning_level",
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#DC2626",
                    "CẦN KIỂM TRA (MEDIUM)": "#D97706",
                    "BÌNH THƯỜNG (LOW)": "#2563EB"
                }
            )
            fig_hist.update_layout(get_clean_plotly_layout(height=340))
            st.plotly_chart(fig_hist, use_container_width=True)

        with sc2:
            st.markdown("""
            <div class="content-box">
                <div class="content-box-title">Tương Quan: Số Mạng Hạ Gục vs Quãng Đường Di Chuyển</div>
            </div>
            """, unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df_anom,
                x="walk_distance",
                y="kills",
                size="anomaly_score",
                color="warning_level",
                hover_data=["player_id", "damage_dealt", "reason"],
                color_discrete_map={
                    "NGUY CƠ CAO (HIGH)": "#DC2626",
                    "CẦN KIỂM TRA (MEDIUM)": "#D97706",
                    "BÌNH THƯỜNG (LOW)": "#2563EB"
                }
            )
            fig_scatter.update_layout(get_clean_plotly_layout(height=340))
            st.plotly_chart(fig_scatter, use_container_width=True)

# =========================================================================
# TRANG 4: TRA CỨU CHI TIẾT TELEMETRY
# =========================================================================
elif selected_page == "4. Tra cứu chi tiết telemetry":
    st.markdown("""
    <div class="header-box">
        <div class="header-title">Tra Cứu Dữ Liệu Chi Tiết Trận Đấu & Người Chơi</div>
        <div class="header-desc">
            Truy vấn theo khóa chính (Primary Key) trong cơ sở dữ liệu Cassandra NoSQL với thời gian đáp ứng milli-giây 
            mà không cần quét tuần tự qua bảng (tránh <code>ALLOW FILTERING</code>).
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_match, tab_player = st.tabs(["Tra cứu Trận Đấu (match_id)", "Tra cứu Người Chơi (player_id)"])

    with tab_match:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">Truy Vấn Bảng Cassandra: match_summary_by_id</div>
        </div>
        """, unsafe_allow_html=True)
        match_summary_all = client.get_match_summary(limit=100)

        if not match_summary_all.empty:
            sample_match_ids = match_summary_all["match_id"].tolist()
            selected_match = st.selectbox("Chọn mã trận đấu mẫu (match_id):", sample_match_ids)
            custom_match = st.text_input("Hoặc nhập chính xác mã trận đấu:", value=selected_match)

            target_match = custom_match.strip() if custom_match.strip() else selected_match
            match_res = client.get_match_summary(match_id=target_match)

            if not match_res.empty:
                m_row = match_res.iloc[0]
                tm1, tm2, tm3, tm4 = st.columns(4)
                tm1.metric("Chế độ chơi", m_row["match_type"])
                tm2.metric("Số người tham gia", f"{m_row['num_players']}")
                tm3.metric("Kills cao nhất trong trận", f"{m_row['max_kills']}")
                tm4.metric("Sát thương cao nhất", f"{m_row['top_damage']:.1f}")

                st.markdown("**Cấu trúc chi tiết bản ghi trận đấu:**")
                st.json({
                    "match_id": m_row["match_id"],
                    "match_type": m_row["match_type"],
                    "duration_seconds": int(m_row["duration_sec"]),
                    "total_knocks": int(m_row["total_knocks"]),
                    "winner_group_id": m_row["winner_group_id"]
                })
            else:
                st.error(f"Không tìm thấy bản ghi cho mã trận đấu: {target_match}")

    with tab_player:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">Truy Vấn Bảng Cassandra: player_record_by_id</div>
        </div>
        """, unsafe_allow_html=True)
        suspicious_sample = client.get_suspicious_records(limit=25)

        if not suspicious_sample.empty:
            sample_player_ids = suspicious_sample["player_id"].tolist()
            selected_player = st.selectbox("Chọn mã người chơi nghi vấn mẫu (player_id):", sample_player_ids)
            custom_player = st.text_input("Hoặc nhập chính xác mã người chơi:", value=selected_player)

            target_player = custom_player.strip() if custom_player.strip() else selected_player
            p_res = client.get_player_records(player_id=target_player)

            if not p_res.empty:
                p_row = p_res.iloc[0]
                tp1, tp2, tp3, tp4 = st.columns(4)
                tp1.metric("Số Hạ Gục (Kills)", f"{p_row['kills']}")
                tp2.metric("Số Headshots", f"{p_row['headshot_kills']}")
                tp3.metric("Tổng Sát Thương", f"{p_row['damage_dealt']:.1f}")
                tp4.metric("Điểm Bất Thường", f"{p_row['anomaly_score']:.1f}")

                st.warning(f"**Giải thích lý do cảnh báo:** {p_row['flagged_reason']}")
                st.dataframe(p_res, use_container_width=True, hide_index=True)
            else:
                st.error(f"Không tìm thấy bản ghi cho mã người chơi: {target_player}")
