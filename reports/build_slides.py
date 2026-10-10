import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Color palette: Esports Big Data Theme
COLOR_DARK_BLUE = RGBColor(14, 28, 54)
COLOR_ORANGE = RGBColor(241, 136, 5)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_LIGHT_BG = RGBColor(245, 247, 250)
COLOR_TEXT_DARK = RGBColor(33, 37, 41)
COLOR_TEXT_MUTED = RGBColor(108, 117, 125)
COLOR_CARD_BG = RGBColor(235, 240, 245)

def add_header(slide, title_text, category_text="ĐỒ ÁN MÔN HỌC: NHẬP MÔN BIG DATA"):
    """Adds a standard branded header to a slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_ORANGE
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_DARK_BLUE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TRANG BÌA (TITLE SLIDE)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK_BLUE
    bg1.line.color.rgb = COLOR_DARK_BLUE

    # Title box
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC NHẬP MÔN DỮ LIỆU LỚN"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ORANGE
    
    p1 = tf1.add_paragraph()
    p1.text = "ỨNG DỤNG APACHE SPARK & CASSANDRA TRONG PHÂN TÍCH DỮ LIỆU PUBG VÀ PHÁT HIỆN DẤU HIỆU GIAN LẬN"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(15)

    p2 = tf1.add_paragraph()
    p2.text = "Phân tích quy mô lớn dữ liệu thể thao điện tử, kỹ nghệ đặc trưng hành vi và trực quan hóa thời gian thực"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(200, 210, 225)
    p2.space_before = Pt(10)

    # Info footer card
    info_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.5))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(24, 43, 73)
    info_card.line.color.rgb = COLOR_ORANGE

    itf = info_card.text_frame
    itf.word_wrap = True
    ip = itf.paragraphs[0]
    ip.text = "GIẢNG VIÊN HƯỚNG DẪN: [ThS. Giảng Viên Hướng Dẫn - Placeholder]"
    ip.font.size = Pt(13)
    ip.font.bold = True
    ip.font.color.rgb = COLOR_WHITE
    
    ip2 = itf.add_paragraph()
    ip2.text = "SINH VIÊN THỰC HIỆN: [Nguyễn Văn A - 20210001] | [Trần Thị B - 20210002] | [Lê Văn C - 20210003]  (Lớp: Nhóm 01)"
    ip2.font.size = Pt(13)
    ip2.font.color.rgb = RGBColor(220, 230, 245)
    ip2.space_before = Pt(8)

    # =========================================================================
    # SLIDE 2: BỐI CẢNH VÀ MỤC TIÊU BÀI TOÁN
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Bối Cảnh Vấn Nạn Gian Lận Esports & Mục Tiêu Bài Toán")
    
    # Left Card: Problem
    c_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = COLOR_CARD_BG
    c_left.line.color.rgb = RGBColor(210, 220, 230)
    ltf = c_left.text_frame
    ltf.word_wrap = True
    
    lp0 = ltf.paragraphs[0]
    lp0.text = "🚨 VẤN NẠN GIAN LẬN TRONG PUBG"
    lp0.font.size = Pt(15)
    lp0.font.bold = True
    lp0.font.color.rgb = RGBColor(180, 50, 20)
    
    lp1 = ltf.add_paragraph()
    lp1.text = "• Tính khốc liệt: 100 người chơi/trận trên bản đồ 8x8 km; 1 kẻ gian lận phá hỏng trải nghiệm của 99 người còn lại."
    lp1.font.size = Pt(13)
    lp1.space_before = Pt(10)

    lp2 = ltf.add_paragraph()
    lp2.text = "• Các hình thức gian lận: Aimbot (tự khóa mục tiêu), Teleport (dịch chuyển), Speed hack, No-recoil, Wallhack."
    lp2.font.size = Pt(13)
    lp2.space_before = Pt(8)

    lp3 = ltf.add_paragraph()
    lp3.text = "• Hạn chế của Anti-Cheat Client: Hacker liên tục vượt qua quét chữ ký bộ nhớ bằng kernel drivers; đòi hỏi giải pháp phân tích máy chủ Big Data."
    lp3.font.size = Pt(13)
    lp3.space_before = Pt(8)

    # Right Card: Objectives
    c_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = COLOR_CARD_BG
    c_right.line.color.rgb = COLOR_ORANGE
    rtf = c_right.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "🎯 MỤC TIÊU CỦA ĐỒ ÁN BIG DATA"
    rp0.font.size = Pt(15)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_DARK_BLUE

    rp1 = rtf.add_paragraph()
    rp1.text = "1. Tải tự động bộ dữ liệu PUBG 4.45M dòng từ Kaggle qua Kaggle CLI."
    rp1.font.size = Pt(13)
    rp1.space_before = Pt(10)

    rp2 = rtf.add_paragraph()
    rp2.text = "2. Xử lý phân tán bằng PySpark: Làm sạch, bảo toàn cực trị, tổng hợp chỉ số."
    rp2.font.size = Pt(13)
    rp2.space_before = Pt(8)

    rp3 = rtf.add_paragraph()
    rp3.text = "3. Phát hiện bất thường bằng PySpark MLlib KMeans & khoảng cách tâm cụm."
    rp3.font.size = Pt(13)
    rp3.space_before = Pt(8)

    rp4 = rtf.add_paragraph()
    rp4.text = "4. Lưu trữ phân tán NoSQL Apache Cassandra phục vụ truy vấn cao tốc."
    rp4.font.size = Pt(13)
    rp4.space_before = Pt(8)

    rp5 = rtf.add_paragraph()
    rp5.text = "5. Xây dựng Dashboard Streamlit 4 trang có giải thích lý do (Explainability)."
    rp5.font.size = Pt(13)
    rp5.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: GIỚI THIỆU BỘ DỮ LIỆU PUBG (KAGGLE DATASET)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Khảo Sát Bộ Dữ Liệu PUBG & Chiến Lược Lấy Mẫu")

    # Data Specs Cards
    specs = [
        ("4,446,966", "Tổng Bản Ghi Gốc", "Dữ liệu người chơi thực tế trong từng trận"),
        ("29 Cột", "Thuộc Tính Schema", "Bao quát chiến đấu, di chuyển, vật phẩm"),
        ("659.5 MB", "Dung Lượng Giải Nén", "Tệp train_V2.csv từ Kaggle Competition"),
        ("1,000 Trận", "Tập Quick Độc Lập", "94,428 bản ghi bảo toàn 100% cấu trúc trận")
    ]
    for i, (val, lbl, desc) in enumerate(specs):
        x = Inches(0.8 + i * 2.95)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_ORANGE
        ctf = card.text_frame
        ctf.word_wrap = True
        p_val = ctf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(22)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_DARK_BLUE
        p_lbl = ctf.add_paragraph()
        p_lbl.text = lbl
        p_lbl.font.size = Pt(12)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_ORANGE
        p_desc = ctf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Explanation
    b_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.8))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = COLOR_CARD_BG
    b_card.line.color.rgb = RGBColor(200, 210, 220)
    btf = b_card.text_frame
    btf.word_wrap = True
    bp0 = btf.paragraphs[0]
    bp0.text = "💡 NGUYÊN TẮC LẤY MẪU CHUẨN SENIOR DATA ENGINEER CHO BATTLE ROYALE:"
    bp0.font.size = Pt(14)
    bp0.font.bold = True
    bp0.font.color.rgb = COLOR_DARK_BLUE
    
    bp1 = btf.add_paragraph()
    bp1.text = "• Không lấy mẫu ngẫu nhiên từng dòng: Trong PUBG, lấy mẫu ngẫu nhiên sẽ làm đứt gãy mối quan hệ đồng đội (groupId) và thứ hạng killPlace (1..100) của trận đấu."
    bp1.space_before = Pt(8)
    bp1.font.size = Pt(13)

    bp2 = btf.add_paragraph()
    bp2.text = "• Lấy mẫu theo cụm matchId nguyên vẹn: Tập `train_quick.csv` giữ nguyên 100% người chơi của 1,000 trận đấu, bảo toàn mọi tương tác hồi sinh (revives), sát thương và tương quan xếp hạng."
    bp2.space_before = Pt(8)
    bp2.font.size = Pt(13)

    bp3 = btf.add_paragraph()
    bp3.text = "• Cấp độ thực thể: Id là mã người chơi trong 1 trận đấu; mô hình hướng tới phát hiện 'Bản ghi trận đấu bất thường', không giả định ID tài khoản xuyên suốt."
    bp3.space_before = Pt(8)
    bp3.font.size = Pt(13)

    # =========================================================================
    # SLIDE 4: CÔNG NGHỆ VÀ CƠ SỞ LÝ THUYẾT
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Ngăn Xếp Công Nghệ Big Data (Technology Stack)")

    techs = [
        ("Apache Spark 4.2.0", "Động cơ xử lý phân tán", [
            "Tính toán In-Memory tốc độ cao",
            "PySpark DataFrame & Spark SQL",
            "Tối ưu hóa Catalyst Optimizer",
            "Spark MLlib huấn luyện phân cụm"
        ]),
        ("Apache Cassandra 4.1", "CSDL NoSQL Phân tán", [
            "Wide-Column Masterless Store",
            "Tối ưu ghi hàng loạt (Batch Statement)",
            "Query-Driven CQL Modeling",
            "Không cần ALLOW FILTERING"
        ]),
        ("Apache Parquet", "Lưu trữ định dạng cột", [
            "Columnar Storage hiệu năng cao",
            "Nén nén Snappy tiết kiệm ổ cứng",
            "Lưu giữ Schema và Metadata chặt chẽ",
            "Chia sẻ dữ liệu giữa Spark & Ingestion"
        ]),
        ("Streamlit + Plotly", "Dashboard & Trực quan", [
            "Giao diện tương tác 4 trang",
            "Biểu đồ phân bố và scatter plot động",
            "Hiển thị cảnh báo & giải thích lý do",
            "Truy vấn trực tiếp CSDL Cassandra"
        ])
    ]

    for i, (title, subtitle, bullets) in enumerate(techs):
        x = Inches(0.8 + i * 2.95)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_DARK_BLUE if i % 2 == 0 else COLOR_ORANGE
        ctf = card.text_frame
        ctf.word_wrap = True
        
        p_t = ctf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_DARK_BLUE
        
        p_s = ctf.add_paragraph()
        p_s.text = subtitle
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = COLOR_ORANGE
        p_s.space_before = Pt(4)

        for b in bullets:
            pb = ctf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(11)
            pb.space_before = Pt(8)

    # =========================================================================
    # SLIDE 5: KIẾN TRÚC TỔNG THỂ HỆ THỐNG
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Kiến Trúc Luồng Dữ Liệu Tổng Thể (End-to-End Pipeline)")

    fig5_path = PROJECT_ROOT / "reports" / "figures" / "architecture_diagram.png"
    if fig5_path.exists():
        slide5.shapes.add_picture(str(fig5_path), Inches(0.8), Inches(1.8), width=Inches(11.7))

    # =========================================================================
    # SLIDE 6: QUY TRÌNH LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Tiền Xử Lý Dữ Liệu & Nguyên Tắc Bảo Toàn Cực Trị")

    # Left card: cleaning
    c1 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_CARD_BG
    c1.line.color.rgb = RGBColor(200, 210, 220)
    tf1 = c1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🧹 LÀM SẠCH DỮ LIỆU CẤU TRÚC"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_BLUE

    items1 = [
        "Kiểm tra tính toàn vẹn khóa: Loại bỏ bản ghi thiếu Id, matchId hoặc groupId.",
        "Xử lý khuyết tật winPlacePerc: Trong 4.45M dòng có chính xác 1 dòng bị null do người chơi ngắt kết nối được lọc bỏ tự động.",
        "Lọc lỗi truyền cảm biến: Khoảng cách âm hoặc thời lượng trận đấu âm bị loại bỏ.",
        "Hiệu năng PySpark: Kiểm tra null bằng PySpark expression phân tán, không tải dữ liệu về Driver bằng collect() vô tội vạ."
    ]
    for it in items1:
        pi = tf1.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(12)
        pi.space_before = Pt(10)

    # Right card: extreme values
    c2 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_CARD_BG
    c2.line.color.rgb = RGBColor(180, 50, 20)
    tf2 = c2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "⚠️ BẢO TOÀN ĐIỂM CỰC TRỊ (EXTREME VALUES)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 50, 20)

    items2 = [
        "Sai lầm phổ biến: Nhiều dự án tự động loại bỏ các điểm ngoại lai (outliers) như 30 kills, 3000 sát thương vì nghĩ là dữ liệu lỗi.",
        "Bản chất bài toán Anomaly: Các chỉ số cực trị đó chính là 'vết tích' quan trọng nhất của các đối tượng sử dụng Aimbot hoặc gian lận!",
        "Nguyên tắc dự án: Giữ lại 100% các giá trị cực đoan để đưa vào thuật toán phân cụm KMeans và tính toán khoảng cách độ lệch.",
        "Độ giữ lại thực tế (Retention Rate): 100.0% trên tập quick và 99.9999% trên tập full."
    ]
    for it in items2:
        pi = tf2.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(12)
        pi.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: PHƯƠNG PHÁP PHÁT HIỆN BẤT THƯỜNG (K-MEANS & DOMAIN RULES)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Giải Thuật Phát Hiện Bất Thường Không Giám Sát (MLlib KMeans)")

    cards = [
        ("1. Kỹ nghệ đặc trưng 8D", "Vector 8 chiều chuẩn hóa:", [
            "kills, damageDealt, headshotKills",
            "longestKill, totalDistance",
            "headshotRate, damagePerKill, killsPerWalkKm"
        ]),
        ("2. Phân cụm KMeans", "Huấn luyện Spark MLlib:", [
            "k = 4 cụm phân tách phong cách thi đấu",
            "Silhouette Score = 0.4665",
            "Xác định tâm cụm C_k đa chiều"
        ]),
        ("3. Khoảng cách Native Catalyst", "Khoảng cách Euclidean:", [
            "Tính toán 100% bằng Spark SQL Catalyst",
            "Ngưỡng phân vị 99.5% d = 6.6916",
            "Khoảng cách cực đại đo được: 104.61"
        ]),
        ("4. Cờ vi phạm vật lý", "Quy luật game PUBG:", [
            "Teleport: >=5 kills nhưng đi bộ <100m",
            "Aimbot: >=8 kills và headshotRate >=85%",
            "Bắn xa phi lý: cự ly hạ gục > 1,000m",
            "Speed: đi bộ vượt giới hạn (>13km)"
        ])
    ]

    for i, (title, sub, bullets) in enumerate(cards):
        x = Inches(0.8 + i * 2.95)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_ORANGE if i == 3 else RGBColor(200, 210, 220)
        ctf = card.text_frame
        ctf.word_wrap = True
        
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_BLUE
        
        ps = ctf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11)
        ps.font.bold = True
        ps.font.color.rgb = COLOR_ORANGE
        ps.space_before = Pt(4)

        for b in bullets:
            pb = ctf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(11)
            pb.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: KẾT QUẢ PHÂN TÍCH TRẬN ĐẤU & TƯƠNG QUAN
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Kết Quả Phân Tích Thống Kê Trận Đấu & Độ Tương Quan")

    fig1_path = PROJECT_ROOT / "reports" / "figures" / "match_modes.png"
    fig2_path = PROJECT_ROOT / "reports" / "figures" / "correlation_heatmap.png"

    if fig1_path.exists() and fig2_path.exists():
        slide8.shapes.add_picture(str(fig1_path), Inches(0.8), Inches(1.8), width=Inches(5.7))
        slide8.shapes.add_picture(str(fig2_path), Inches(6.8), Inches(1.8), width=Inches(5.7))

    # =========================================================================
    # SLIDE 9: DASHBOARD STREAMLIT VÀ KẾT QUẢ CẢNH BÁO
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Giao Diện Dashboard Streamlit & Cảnh Báo Anomaly")

    fig4_path = PROJECT_ROOT / "reports" / "figures" / "combat_scatter.png"
    if fig4_path.exists():
        slide9.shapes.add_picture(str(fig4_path), Inches(0.8), Inches(1.8), width=Inches(6.2))

    # Right Card: Explainability showcase
    c_exp = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.8), Inches(5.2), Inches(5.0))
    c_exp.fill.solid()
    c_exp.fill.fore_color.rgb = COLOR_CARD_BG
    c_exp.line.color.rgb = COLOR_ORANGE
    etf = c_exp.text_frame
    etf.word_wrap = True

    ep = etf.paragraphs[0]
    ep.text = "🎯 CƠ CHẾ EXPLAINABILITY MINH BẠCH"
    ep.font.size = Pt(14)
    ep.font.bold = True
    ep.font.color.rgb = COLOR_DARK_BLUE

    cases = [
        "Phát hiện 482 / 94,428 bản ghi (0.510%) có dấu hiệu bất thường rõ rệt.",
        "Case 1 (Aimbot): 14 kills, 12 headshots (85.7%), sát thương 2,554.0. Điểm khoảng cách: 22.51.",
        "Case 2 (Aimbot): 14 kills, 13 headshots (92.9% headshot rate!).",
        "Case 3 (Teleport): 1 kill nhưng đi bộ 0.0m. Điểm khoảng cách tới tâm cụm lên tới 104.61.",
        "Lợi ích: Trọng tài giải đấu biết chính xác lý do cảnh báo thay vì phán đoán mơ hồ."
    ]
    for c in cases:
        pc = etf.add_paragraph()
        pc.text = f"• {c}"
        pc.font.size = Pt(11)
        pc.space_before = Pt(8)

    # =========================================================================
    # SLIDE 10: ĐÁNH GIÁ THỰC NGHIỆM VÀ HIỆU NĂNG
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Đo Lường Hiệu Năng Thực Tế (Benchmark Đo Lường Thực Tế)")

    table_shape = slide10.shapes.add_table(rows=8, cols=4, left=Inches(0.8), top=Inches(1.8), width=Inches(11.7), height=Inches(4.8))
    table = table_shape.table

    b_data = [
        ("Giai đoạn Pipeline", "Công nghệ thực thi", "Thời gian (s)", "Tỷ lệ"),
        ("1. Nạp dữ liệu CSV", "PySpark CSV Reader với Schema", "1.45 s", "2.3%"),
        ("2. Tiền xử lý & Làm sạch", "PySpark Filter & Validation", "5.94 s", "9.3%"),
        ("3. Phân tích thống kê trận đấu", "Spark SQL & Window Functions", "5.25 s", "8.2%"),
        ("4. Kỹ nghệ đặc trưng hành vi", "VectorAssembler & StandardScaler", "2.73 s", "4.3%"),
        ("5. Huấn luyện KMeans MLlib", "PySpark MLlib & Catalyst Distance", "22.96 s", "35.8%"),
        ("6. Ghi định dạng Parquet", "Spark Parquet Writer (Snappy)", "18.12 s", "28.3%"),
        ("7. Ingest vào CSDL Cassandra", "Cassandra Batch Ingestion", "7.58 s", "11.8%")
    ]

    for r_idx, row in enumerate(b_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            if r_idx == 0:
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_ORANGE
            else:
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 11: HẠN CHẾ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Hạn Chế Học Thuật & Định Hướng Mở Rộng")

    c1 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_CARD_BG
    c1.line.color.rgb = RGBColor(180, 50, 20)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⚠️ HẠN CHẾ & THÁCH THỨC ĐẠO ĐỨC DỮ LIỆU"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 50, 20)

    limits = [
        "Thiếu nhãn Ground-Truth: Bộ dữ liệu Kaggle không có nhãn ban nick chính thức. Báo cáo Precision/Recall có giám sát là phi khoa học.",
        "Nguy cơ False Positives: Tuyển thủ chuyên nghiệp (Pro-players) có thể đạt chỉ số sát thương và headshot vượt trội mà không gian lận.",
        "Phạm vi định danh: Id chỉ là định danh trong trận; không thể theo dõi hành vi xuyên suốt nhiều ngày nếu thiếu Steam Account ID.",
        "Độ trễ mạng (Desync): Hiện tượng lag mạng có thể gây sai lệch cảm biến vị trí người chơi."
    ]
    for lim in limits:
        pl = tf1.add_paragraph()
        pl.text = f"• {lim}"
        pl.font.size = Pt(12)
        pl.space_before = Pt(8)

    c2 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_CARD_BG
    c2.line.color.rgb = COLOR_DARK_BLUE
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🚀 ĐỊNH HƯỚNG PHÁT TRIỂN TƯƠNG LAI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_BLUE

    future = [
        "Spark Streaming + Kafka: Xử lý luồng telemetry logs theo thời gian thực ngay khi trận đấu đang diễn ra.",
        "Deep Learning chuỗi thời gian: Dùng LSTM / Transformer phân tích chuỗi tọa độ (X, Y, Z) để phát hiện hành vi Wallhack/ESP nhìn xuyên tường.",
        "Cơ chế Feedback Loop: Tích hợp nút duyệt của trọng tài trên Streamlit để gắn nhãn thủ công, xây dựng tập ground-truth phục vụ mô hình bán giám sát (Semi-supervised)."
    ]
    for fut in future:
        pf = tf2.add_paragraph()
        pf.text = f"• {fut}"
        pf.font.size = Pt(12)
        pf.space_before = Pt(10)

    # =========================================================================
    # SLIDE 12: KẾT LUẬN VÀ HỎI ĐÁP (CONCLUSION & Q&A)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = COLOR_DARK_BLUE
    bg12.line.color.rgb = COLOR_DARK_BLUE

    t_box12 = slide12.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.0))
    tf12 = t_box12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "TỔNG KẾT ĐỀ TÀI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    p1 = tf12.add_paragraph()
    p1.text = "HỆ THỐNG PHÂN TÍCH BIG DATA PUBG & PHÁT HIỆN BẤT THƯỜNG HOÀN TẤT 100%"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(10)

    summary = [
        "1. Làm chủ công nghệ cốt lõi: PySpark tính toán phân tán + Cassandra NoSQL lưu trữ cao tốc.",
        "2. Giải thuật thực tiễn: K-Means MLlib phối hợp cờ vật lý, phát hiện 482 ca bất thường có diễn giải.",
        "3. Trực quan hóa hiện đại: Dashboard Streamlit 4 trang kết nối cơ sở dữ liệu thực.",
        "4. Kịch bản chạy mượt mà: Hoàn tất toàn bộ pipeline trong 64 giây ở chế độ Quick, sẵn sàng bảo vệ."
    ]
    for s in summary:
        ps = tf12.add_paragraph()
        ps.text = f"✔ {s}"
        ps.font.size = Pt(14)
        ps.font.color.rgb = RGBColor(220, 235, 255)
        ps.space_before = Pt(8)

    p_qa = tf12.add_paragraph()
    p_qa.text = "CẢM ƠN THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE! XIN MỜI ĐẶT CÂU HỎI (Q&A)"
    p_qa.font.size = Pt(18)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_ORANGE
    p_qa.space_before = Pt(25)

    # Save Presentation
    output_pptx = PROJECT_ROOT / "reports" / "slides.pptx"
    prs.save(str(output_pptx))
    print(f">>> Đã tạo thành công bộ Slide thuyết trình 12 trang tại: {output_pptx} (Dung lượng: {output_pptx.stat().st_size:,} bytes)")

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    create_presentation()
