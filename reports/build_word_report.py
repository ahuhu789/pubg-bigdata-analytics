import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def set_cell_background(cell, fill_hex):
    """Sets cell background color."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding inside cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()
    
    # Page setup - Standard A4 with 2.5cm margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style configuration
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 1. TRANG BÌA (COVER PAGE)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC [TÊN TRƯỜNG - PLACEHOLDER]\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    run.font.size = Pt(13)
    run.font.bold = True
    
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_line = p_line.add_run("-------------------***-------------------\n\n\n")
    run_line.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_title.add_run("BÁO CÁO ĐỒ ÁN MÔN HỌC\nNHẬP MÔN DỮ LIỆU LỚN (BIG DATA)\n\n")
    run_sub.font.size = Pt(15)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0, 51, 102)

    run_main = p_title.add_run("ỨNG DỤNG APACHE SPARK VÀ CASSANDRA TRONG PHÂN TÍCH DỮ LIỆU TRẬN ĐẤU PUBG VÀ PHÁT HIỆN NGƯỜI CHƠI CÓ DẤU HIỆU GIAN LẬN TRONG THỂ THAO ĐIỆN TỬ\n\n\n")
    run_main.font.size = Pt(18)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(180, 50, 20)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.5)
    
    r = p_info.add_run("Giảng viên hướng dẫn:\t")
    r.bold = True
    p_info.add_run("[ThS. Giảng Viên Hướng Dẫn - Placeholder]\n")
    
    r = p_info.add_run("Sinh viên thực hiện:\t\n")
    r.bold = True
    p_info.add_run("1. [Nguyễn Văn A] - MSSV: [20210001] (Nhóm trưởng)\n")
    p_info.add_run("2. [Trần Thị B]   - MSSV: [20210002]\n")
    p_info.add_run("3. [Lê Văn C]     - MSSV: [20210003]\n\n")
    
    r = p_info.add_run("Lớp học phần:\t\t")
    r.bold = True
    p_info.add_run("[Nhập môn Big Data - Nhóm 01]\n")
    
    r = p_info.add_run("Niên khóa / Học kỳ:\t")
    r.bold = True
    p_info.add_run("Học kỳ 1 - Năm học 2026-2027\n\n\n")

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_loc.add_run("TP. HỒ CHÍ MINH, THÁNG 10/2026")
    r_loc.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 2. LỊCH LÀM VIỆC NHÓM HẰNG TUẦN (WEEKLY SCHEDULE)
    # =========================================================================
    h1 = doc.add_heading("LỊCH LÀM VIỆC NHÓM HẰNG TUẦN", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    doc.add_paragraph(
        "Dưới đây là kế hoạch chi tiết và tiến độ thực hiện đề tài qua các tuần làm việc của nhóm. "
        "Kế hoạch được lập theo dạng biểu mẫu có thể tùy chỉnh thông tin:"
    )

    schedule_data = [
        ("Tuần", "Nội dung công việc", "Người phụ trách", "Sản phẩm bàn giao", "Trạng thái"),
        ("Tuần 1", "Khảo sát đề tài, tìm hiểu bài toán esports PUBG, cài đặt môi trường Spark và Kaggle CLI", "Cả nhóm", "Môi trường hoàn chỉnh, repo dự án", "Hoàn thành"),
        ("Tuần 2", "Tìm kiếm, khảo sát và tải bộ dữ liệu PUBG từ Kaggle; Phân tích cấu trúc schema và khóa định danh", "Thành viên A", "Dataset train_V2.csv (4.45M dòng), train_quick.csv", "Hoàn thành"),
        ("Tuần 3", "Xây dựng pipeline PySpark: Kiểm tra chất lượng dữ liệu, xử lý giá trị khuyết và bảo toàn cực trị", "Thành viên B", "Module preprocessing.py, unit tests", "Hoàn thành"),
        ("Tuần 4", "Phân tích thống kê dữ liệu trận đấu và các chế độ chơi bằng Spark SQL & Window Functions", "Thành viên C", "Module match_analytics.py, Parquet export", "Hoàn thành"),
        ("Tuần 5", "Kỹ nghệ đặc trưng hành vi (Feature Engineering): Headshot rate, Damage/Kill, Di chuyển", "Thành viên A, B", "Module feature_engineering.py", "Hoàn thành"),
        ("Tuần 6", "Nghiên cứu và triển khai mô hình học máy PySpark MLlib KMeans, tính khoảng cách tâm cụm", "Thành viên A", "Module anomaly_detection.py, Anomaly Scoring", "Hoàn thành"),
        ("Tuần 7", "Thiết kế schema NoSQL Apache Cassandra (init.cql), xây dựng Cassandra Client & fallback", "Thành viên B", "Module cassandra_client.py, Docker Compose", "Hoàn thành"),
        ("Tuần 8", "Xây dựng Dashboard trực quan hóa 4 trang bằng Streamlit kết nối dữ liệu Cassandra", "Thành viên C", "dashboard/app.py, biểu đồ tương tác", "Hoàn thành"),
        ("Tuần 9", "Thực nghiệm toàn diện chế độ Quick & Full, đo lường thời gian thực thi, thu thập số liệu", "Cả nhóm", "reports/experiment_results.md", "Hoàn thành"),
        ("Tuần 10", "Viết báo cáo tổng kết Word, thiết kế Slide thuyết trình, chuẩn bị kịch bản bảo vệ demo", "Cả nhóm", "report.docx, slides.pptx, README.md", "Hoàn thành")
    ]

    table_sched = doc.add_table(rows=len(schedule_data), cols=5)
    table_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(schedule_data):
        for c_idx, val in enumerate(row):
            cell = table_sched.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 80, 80, 100, 100)
            if r_idx == 0:
                set_cell_background(cell, "003366")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F5F5F5")
                p = cell.paragraphs[0]
                p.runs[0].font.size = Pt(11)

    doc.add_paragraph()

    # =========================================================================
    # 3. PHÂN CÔNG NHIỆM VỤ THÀNH VIÊN
    # =========================================================================
    h1 = doc.add_heading("BẢNG PHÂN CÔNG CÔNG VIỆC TỪNG THÀNH VIÊN", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    member_data = [
        ("STT", "Họ và Tên", "MSSV", "Vai trò", "Nhiệm vụ chính phụ trách", "Tỷ lệ đóng góp"),
        ("1", "[Nguyễn Văn A]", "[20210001]", "Nhóm trưởng", "Kiến trúc hệ thống Big Data, PySpark MLlib KMeans, Pipeline Orchestration, Báo cáo", "100%"),
        ("2", "[Trần Thị B]", "[20210002]", "Thành viên", "Tiền xử lý dữ liệu PySpark, Thiết kế CSDL Apache Cassandra, Ingestion Client, Slide", "100%"),
        ("3", "[Lê Văn C]", "[20210003]", "Thành viên", "Phân tích thống kê Spark SQL, Xây dựng Dashboard Streamlit, Kiểm thử thực nghiệm", "100%")
    ]

    table_mem = doc.add_table(rows=len(member_data), cols=6)
    table_mem.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(member_data):
        for c_idx, val in enumerate(row):
            cell = table_mem.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 80, 80, 100, 100)
            if r_idx == 0:
                set_cell_background(cell, "003366")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                p = cell.paragraphs[0]
                p.runs[0].font.size = Pt(11)
                if c_idx in [0, 2, 5]:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # =========================================================================
    # 4. MỤC LỤC TỔNG QUAN
    # =========================================================================
    h1 = doc.add_heading("MỤC LỤC BÁO CÁO", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    toc_items = [
        ("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI", "Trang 1"),
        ("   1.1. Bối cảnh và Tính cấp thiết của Bài toán Esports", "Trang 1"),
        ("   1.2. Mục tiêu Nghiên cứu của Đồ án", "Trang 2"),
        ("   1.3. Phạm vi và Đối tượng Nghiên cứu", "Trang 2"),
        ("   1.4. Ý nghĩa Khoa học và Giá trị Ứng dụng Thực tiễn", "Trang 3"),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ BIG DATA", "Trang 4"),
        ("   2.1. Tổng quan về Dữ liệu lớn (Big Data)", "Trang 4"),
        ("   2.2. Apache Spark và Động cơ Tính toán Phân tán", "Trang 5"),
        ("   2.3. Thuật toán Phân cụm K-Means trong Spark MLlib", "Trang 7"),
        ("   2.4. Cơ sở Dữ liệu NoSQL Apache Cassandra", "Trang 8"),
        ("   2.5. Framework Trực quan hóa Dữ liệu Streamlit", "Trang 10"),
        ("CHƯƠNG 3: KHẢO SÁT, TIỀN XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU PUBG", "Trang 11"),
        ("   3.1. Thu thập Dữ liệu qua Kaggle CLI", "Trang 11"),
        ("   3.2. Cấu trúc Schema và Ý nghĩa các Thuộc tính", "Trang 12"),
        ("   3.3. Quy trình Làm sạch và Nguyên tắc Bảo toàn Cực trị", "Trang 13"),
        ("   3.4. Phân tích Thống kê Phân tán theo Chế độ chơi", "Trang 14"),
        ("CHƯƠNG 4: THIẾT KẾ KIẾN TRÚC HỆ THỐNG BIG DATA", "Trang 16"),
        ("   4.1. Kiến trúc Tổng thể Pipeline (Pipeline Architecture)", "Trang 16"),
        ("   4.2. Thiết kế Mô hình Dữ liệu NoSQL Cassandra (CQL Modeling)", "Trang 17"),
        ("   4.3. Cơ chế Khả năng Phục hồi (Fault Resilience) và Persistent Fallback", "Trang 19"),
        ("CHƯƠNG 5: MÔ HÌNH HỌC MÁY VÀ PHÁT HIỆN BẤT THƯỜNG", "Trang 20"),
        ("   5.1. Kỹ nghệ Đặc trưng Hành vi Thi đấu (Feature Engineering)", "Trang 20"),
        ("   5.2. Chuẩn hóa Vector và Huấn luyện Spark MLlib KMeans", "Trang 21"),
        ("   5.3. Tính toán Khoảng cách và Công thức Điểm Bất thường (Anomaly Score)", "Trang 22"),
        ("   5.4. Cơ chế Giải thích Lý do Cảnh báo (Explainable AI)", "Trang 23"),
        ("CHƯƠNG 6: THỰC NGHIỆM, KẾT QUẢ VÀ TRỰC QUAN HÓA", "Trang 24"),
        ("   6.1. Thiết lập Môi trường và Kịch bản Thực nghiệm", "Trang 24"),
        ("   6.2. Kết quả Đo lường Hiệu năng Thực tế (Benchmark)", "Trang 25"),
        ("   6.3. Phân tích Các Trường hợp Nghi vấn Điển hình (Case Studies)", "Trang 26"),
        ("   6.4. Giao diện Dashboard Trực quan hóa Streamlit", "Trang 27"),
        ("CHƯƠNG 7: THẢO LUẬN, GIỚI HẠN VÀ ĐẠO ĐỨC DỮ LIỆU", "Trang 29"),
        ("   7.1. Phân biệt Giữa Thống kê Bất thường và Kết luận Gian lận", "Trang 29"),
        ("   7.2. Thách thức Thiếu Nhãn Ground-Truth và Nguy cơ Dương tính Giả", "Trang 30"),
        ("CHƯƠNG 8: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", "Trang 31"),
        ("TÀI LIỆU THAM KHẢO", "Trang 32")
    ]

    for item, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.15
        p_toc.paragraph_format.space_after = Pt(2)
        r1 = p_toc.add_run(item)
        if item.startswith("CHƯƠNG"):
            r1.font.bold = True
        r2 = p_toc.add_run(f"\t{page}")
        r2.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI
    # =========================================================================
    doc.add_heading("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI", level=1)
    
    doc.add_heading("1.1. Bối cảnh và Tính cấp thiết của Bài toán Esports", level=2)
    doc.add_paragraph(
        "Trong thập kỷ qua, Thể thao Điện tử (Esports) đã chứng kiến sự phát triển bùng nổ, trở thành một ngành công nghiệp giải trí "
        "trị giá hàng tỷ USD với hàng trăm triệu khán giả trên toàn cầu. Trong số các tựa game bắn súng sinh tồn (Battle Royale), "
        "PlayerUnknown's Battlegrounds (PUBG) do Krafton và PUBG Corporation phát hành là một trong những cột mốc định hình thể loại này. "
        "Một trận đấu PUBG tiêu chuẩn quy tụ tới 100 người chơi trên một hòn đảo rộng lớn (8x8 km), nơi người chơi phải tự tìm kiếm vũ khí, "
        "trang bị, di chuyển vào vùng an toàn và chiến đấu để trở thành người hoặc đội sống sót cuối cùng."
    )
    doc.add_paragraph(
        "Tuy nhiên, sự thành công rực rỡ của PUBG cũng đi kèm với vấn nạn nhức nhối nhất trong lịch sử esports: phần mềm gian lận (cheat/hack). "
        "Các công cụ gian lận phổ biến như tự động ngắm bắn chuẩn xác (Aimbot), dịch chuyển tức thời (Teleport), chạy siêu tốc (Speed hack), "
        "nhìn xuyên vật thể (Wallhack/ESP), hay loại bỏ độ giật súng (No-recoil) đã phá hủy tính công bằng, gây ức chế sâu sắc cho cộng đồng "
        "và đe dọa trực tiếp đến tính toàn vẹn của các giải đấu chuyên nghiệp."
    )
    doc.add_paragraph(
        "Mỗi ngày, hệ thống máy chủ của PUBG sản sinh ra hàng terabyte dữ liệu nhật ký trận đấu (telemetry logs, combat events). "
        "Các giải pháp chống gian lận truyền thống cài đặt trên máy người dùng (như BattlEye, Easy Anti-Cheat) hoạt động dựa trên cơ chế "
        "quét chữ ký bộ nhớ (signature scanning) và thường xuyên bị hacker qua mặt thông qua việc can thiệp kernel-level drivers. "
        "Do đó, phương pháp tiếp cận từ phía máy chủ thông qua Phân tích Dữ liệu Lớn (Big Data Analytics) và Học máy phân tích hành vi "
        "nổi lên như một lá chắn thứ hai mang tính sống còn: phát hiện những hành vi thi đấu bất thường về mặt thống kê và vi phạm "
        "các quy luật vật lý của trò chơi."
    )

    doc.add_heading("1.2. Mục tiêu Nghiên cứu của Đồ án", level=2)
    doc.add_paragraph(
        "Đề tài hướng tới việc thiết kế và hiện thực hóa một ứng dụng Big Data hoàn chỉnh, vận hành thực tế trên môi trường máy tính cá nhân, "
        "phục vụ các mục tiêu trọng tâm sau:"
    )
    doc.add_paragraph(
        "1. Thu thập dữ liệu thực tế: Sử dụng Kaggle CLI để tự động tải bộ dữ liệu PUBG chính thức quy mô lớn (hơn 4.44 triệu bản ghi).\n"
        "2. Xử lý dữ liệu lớn phân tán: Áp dụng Apache Spark (PySpark DataFrame, Spark SQL) để làm sạch, kiểm tra chất lượng, tổng hợp thống kê và kỹ nghệ đặc trưng hành vi.\n"
        "3. Phát hiện bất thường không giám sát: Xây dựng giải thuật học máy PySpark MLlib K-Means kết hợp đo lường khoảng cách Euclidean tới tâm cụm và các cờ kiểm tra giới hạn vật lý để lọc ra các bản ghi thi đấu bất thường.\n"
        "4. Lưu trữ phân tán NoSQL: Thiết kế lược đồ NoSQL trên Apache Cassandra (CQL) tối ưu hóa theo các mẫu truy vấn tra cứu cao tốc của dashboard.\n"
        "5. Trực quan hóa trực quan: Phát triển Dashboard tương tác bằng Streamlit cung cấp 4 trang nghiệp vụ chuyên sâu phục vụ giám sát và tra cứu chi tiết."
    )

    doc.add_heading("1.3. Phạm vi và Đối tượng Nghiên cứu", level=2)
    doc.add_paragraph(
        "- Phạm vi tựa game: Đề tài tập trung duy nhất vào tựa game PlayerUnknown's Battlegrounds (PUBG). Tuyệt đối không chuyển sang các game khác.\n"
        "- Đối tượng dữ liệu: Bộ dữ liệu công khai từ giải đấu PUBG Finish Placement Prediction trên Kaggle, chứa 29 thuộc tính bao quát toàn bộ chỉ số chiến đấu, di chuyển, vật phẩm và xếp hạng của người chơi.\n"
        "- Cấp độ thực thể: Bản ghi người chơi trong từng trận đấu cụ thể (Player-Match Record). Đề tài định nghĩa rõ ràng đây là phân tích hành vi bất thường theo phiên thi đấu, không tự bịa đặt ID tài khoản xuyên suốt."
    )

    doc.add_heading("1.4. Ý nghĩa Khoa học và Giá trị Ứng dụng Thực tiễn", level=2)
    doc.add_paragraph(
        "Đề tài minh chứng rõ nét năng lực phối hợp giữa tính toán phân tán (Apache Spark) và lưu trữ NoSQL hướng cột phân tán (Apache Cassandra). "
        "Hệ thống không chỉ dừng lại ở các báo cáo thống kê tĩnh mà cung cấp một giải pháp Explainable AI (AI có khả năng giải thích lý do), "
        "giúp ban trọng tài esports và nhà phát hành game dễ dàng nắm bắt nguyên nhân một bản ghi bị cảnh báo (ví dụ: tỷ lệ headshot 92.9% hay đi bộ 0m nhưng có mạng hạ gục)."
    )

    # =========================================================================
    # CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ BIG DATA
    # =========================================================================
    doc.add_heading("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ BIG DATA", level=1)
    
    doc.add_heading("2.1. Tổng quan về Dữ liệu lớn (Big Data)", level=2)
    doc.add_paragraph(
        "Dữ liệu lớn (Big Data) được định nghĩa bởi mô hình 5V kinh điển:\n"
        "- Volume (Khối lượng): Quy mô dữ liệu vượt quá khả năng lưu trữ và xử lý của các hệ quản trị CSDL quan hệ truyền thống trên một máy đơn lẻ. Trong PUBG, hàng triệu trận đấu tạo ra hàng tỷ điểm dữ liệu.\n"
        "- Velocity (Vận tốc): Dữ liệu được sinh ra với tốc độ cực nhanh trong thời gian thực sau mỗi trận đấu.\n"
        "- Variety (Đa dạng): Dữ liệu bao gồm sự kiện chiến đấu, tọa độ di chuyển, thời gian, thuộc tính định danh.\n"
        "- Veracity (Tính xác thực): Sự tồn tại của dữ liệu nhiễu, lỗi mạng, mất gói tin đòi hỏi quy trình tiền xử lý nghiêm ngặt.\n"
        "- Value (Giá trị): Mục tiêu cốt lõi là trích xuất tri thức, phát hiện các mẫu hành vi bất thường nhằm bảo vệ tính công bằng của tựa game."
    )

    doc.add_heading("2.2. Apache Spark và Động cơ Tính toán Phân tán", level=2)
    doc.add_paragraph(
        "Apache Spark là nền tảng tính toán phân tán mã nguồn mở hàng đầu hiện nay, cung cấp khả năng xử lý dữ liệu trong bộ nhớ (In-Memory Processing) "
        "nhanh hơn tới 100 lần so với mô hình Hadoop MapReduce truyền thống. Kiến trúc Spark bao gồm:\n"
        "- Driver Program: Chịu trách nhiệm khởi tạo SparkSession, phân tích đồ thị luồng công việc (DAG - Directed Acyclic Graph) và điều phối công việc tới các worker.\n"
        "- Cluster Manager: Quản lý tài nguyên hệ thống (Local, YARN, Mesos hoặc Kubernetes).\n"
        "- Executors: Các tiến trình chạy trên worker node chịu trách nhiệm thực thi các tác vụ tính toán và lưu trữ dữ liệu phân mảnh.\n"
        "- Catalyst Optimizer: Bộ tối ưu hóa truy vấn nâng cao của Spark SQL, tự động tối ưu hóa cây logic (Logical Plan) thành cây thực thi vật lý (Physical Plan) hiệu quả cao."
    )

    doc.add_heading("2.3. Thuật toán Phân cụm K-Means trong Spark MLlib", level=2)
    doc.add_paragraph(
        "Spark MLlib là thư viện học máy phân tán xây dựng trên nền tảng Spark. Trong đề tài này, thuật toán K-Means Clustering được lựa chọn "
        "để phân tách quần thể người chơi thành k cụm hành vi tự nhiên trong không gian đa chiều. Hàm mục tiêu của K-Means là tối thiểu hóa "
        "tổng bình phương khoảng cách từ mỗi điểm dữ liệu x_i đến tâm cụm gần nhất c_k:\n\n"
        "      J = SUM_{k=1}^K SUM_{x_i in S_k} || x_i - c_k ||^2\n\n"
        "Sau khi các tâm cụm được xác định, khoảng cách Euclidean từ mỗi vector quan sát tới tâm cụm của nó đóng vai trò là cơ sở để đo lường "
        "độ lệch chuẩn (Anomaly Score). Những người chơi có khoảng cách vượt qua ngưỡng phân vị 99.5% là những cá thể nằm ở rìa ngoại lai, "
        "thể hiện phong cách thi đấu dị biệt."
    )

    doc.add_heading("2.4. Cơ sở Dữ liệu NoSQL Apache Cassandra", level=2)
    doc.add_paragraph(
        "Apache Cassandra là hệ quản trị cơ sở dữ liệu phân tán NoSQL dạng Wide-Column Store, được thiết kế theo kiến trúc phi tập trung (Peer-to-Peer, Masterless). "
        "Cassandra tối ưu hóa tuyệt đối cho các tác vụ ghi khối lượng lớn với độ trễ thấp và khả năng mở rộng quy mô tuyến tính (Linear Scalability). "
        "Nguyên tắc cốt lõi khi thiết kế cơ sở dữ liệu Cassandra là 'Query-Driven Modeling': các bảng được thiết kế trực tiếp dựa trên các câu truy vấn "
        "của ứng dụng thông qua Khóa phân vùng (Partition Key) và Khóa sắp xếp (Clustering Key), loại bỏ hoàn toàn các phép JOIN phức tạp."
    )

    doc.add_heading("2.5. Framework Trực quan hóa Dữ liệu Streamlit", level=2)
    doc.add_paragraph(
        "Streamlit là thư viện mã nguồn mở nền Python cho phép xây dựng nhanh chóng các ứng dụng web tương tác phục vụ Data Science và Machine Learning. "
        "Kết hợp với thư viện đồ họa tương tác Plotly, giao diện Streamlit kết nối trực tiếp với Cassandra để tải dữ liệu và cung cấp bộ lọc động đa chiều."
    )

    # =========================================================================
    # CHƯƠNG 3: KHẢO SÁT, TIỀN XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU PUBG
    # =========================================================================
    doc.add_heading("CHƯƠNG 3: KHẢO SÁT, TIỀN XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU PUBG", level=1)
    
    doc.add_heading("3.1. Thu thập Dữ liệu qua Kaggle CLI", level=2)
    doc.add_paragraph(
        "Dữ liệu được thu thập chính thức bằng công cụ dòng lệnh Kaggle CLI từ cuộc thi PUBG Finish Placement Prediction:\n"
        "Lệnh tải dữ liệu:\n"
        "      kaggle competitions download -c pubg-finish-placement-prediction -f train_V2.csv -p data/raw\n"
        "Tập tin nén `train_V2.csv.zip` có dung lượng 244 MB, sau khi giải nén đạt 659.5 MB, gồm 4,446,966 bản ghi và 29 cột thuộc tính."
    )

    doc.add_heading("3.2. Cấu trúc Schema và Ý nghĩa các Thuộc tính", level=2)
    doc.add_paragraph(
        "Các nhóm thuộc tính chính trong bộ dữ liệu:\n"
        "- Nhóm định danh: `Id` (mã bản ghi người chơi), `groupId` (mã đội trong trận), `matchId` (mã trận đấu).\n"
        "- Nhóm chiến đấu: `kills` (số mạng hạ gục), `damageDealt` (tổng sát thương gây ra), `headshotKills` (hạ gục bằng bắn vào đầu), `killStreaks` (chuỗi hạ gục liên tiếp), `longestKill` (khoảng cách hạ gục xa nhất).\n"
        "- Nhóm di chuyển: `walkDistance` (khoảng cách đi bộ, mét), `rideDistance` (khoảng cách lái xe), `swimDistance` (khoảng cách bơi).\n"
        "- Nhóm hỗ trợ & Sinh tồn: `heals` (băng gạc/hộp sơ cứu), `boosts` (nước tăng lực/thuốc giảm đau), `revives` (cứu đồng đội), `DBNOs` (hạ gục đối thủ nhưng chưa chết hẳn).\n"
        "- Nhóm trận đấu & Kết quả: `matchType` (chế độ chơi: squad, duo, solo, squad-fpp...), `matchDuration` (thời lượng trận đấu tính bằng giây), `winPlacePerc` (thứ hạng chuẩn hóa từ 0.0 đến 1.0)."
    )

    doc.add_heading("3.3. Quy trình Làm sạch và Nguyên tắc Bảo toàn Cực trị", level=2)
    doc.add_paragraph(
        "Khác với các bài toán học máy thông thường - nơi các giá trị ngoại lai (outliers) thường bị loại bỏ để tránh làm sai lệch mô hình dự đoán - "
        "trong bài toán Phát hiện gian lận và Hành vi bất thường, các điểm cực trị (như người chơi có 30 mạng hạ gục, 3000 sát thương) "
        "chính là ĐỐI TƯỢNG HẠT NHÂN CẦN PHÂN TÍCH. Quy tắc làm sạch của nhóm tuân thủ nghiêm ngặt:\n"
        "- Chỉ loại bỏ các bản ghi lỗi cấu trúc: thiếu `Id`, thiếu `matchId` hoặc thiếu `winPlacePerc` (có chính xác 1 dòng trong dataset 4.45M dòng).\n"
        "- Loại bỏ các giá trị sai do lỗi cảm biến truyền tải: khoảng cách âm, số kills âm, hoặc thời lượng trận đấu âm.\n"
        "- Bảo toàn tuyệt đối mọi bản ghi có chỉ số chiến đấu cao phi thường."
    )

    doc.add_heading("3.4. Phân tích Thống kê Phân tán theo Chế độ chơi", level=2)
    doc.add_paragraph(
        "Kết quả phân tích thống kê phân tán trên tập dữ liệu được tổng hợp bằng PySpark và lưu trữ trong bảng `analytics_by_match_type`. "
        "Chế độ `squad-fpp` (đội 4 người góc nhìn thứ nhất) chiếm tỷ trọng lớn nhất với 421 trận và 39,889 người chơi, kế đến là `duo-fpp` và `squad`."
    )

    # Insert Figure 1
    fig1_path = PROJECT_ROOT / "reports" / "figures" / "match_modes.png"
    if fig1_path.exists():
        doc.add_paragraph()
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(fig1_path), width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run("Hình 1: Phân bố số lượng người chơi theo chế độ chơi PUBG (Thống kê Spark SQL)")
        run_cap.font.italic = True
        run_cap.font.size = Pt(11)

    # Insert Figure 2
    fig2_path = PROJECT_ROOT / "reports" / "figures" / "correlation_heatmap.png"
    if fig2_path.exists():
        doc.add_paragraph()
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(fig2_path), width=Inches(5.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run("Hình 2: Ma trận tương quan Pearson giữa các chỉ số thi đấu với thứ hạng cuối trận")
        run_cap.font.italic = True
        run_cap.font.size = Pt(11)

    # =========================================================================
    # CHƯƠNG 4: THIẾT KẾ KIẾN TRÚC HỆ THỐNG BIG DATA
    # =========================================================================
    doc.add_heading("CHƯƠNG 4: THIẾT KẾ KIẾN TRÚC HỆ THỐNG BIG DATA", level=1)
    
    doc.add_heading("4.1. Kiến trúc Tổng thể Pipeline", level=2)
    doc.add_paragraph(
        "Hệ thống được thiết kế theo luồng xử lý phân tầng tuần tự (Pipeline Architecture) gồm 5 tầng công nghệ:"
    )

    fig5_path = PROJECT_ROOT / "reports" / "figures" / "architecture_diagram.png"
    if fig5_path.exists():
        doc.add_paragraph()
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(fig5_path), width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run("Hình 3: Sơ đồ kiến trúc tổng thể hệ thống Big Data (Spark - Parquet - Cassandra - Streamlit)")
        run_cap.font.italic = True
        run_cap.font.size = Pt(11)

    doc.add_paragraph(
        "1. Tầng Thu thập (Ingestion Layer): Kaggle CLI tải trực tiếp các tệp dữ liệu thô vào thư mục `data/raw`.\n"
        "2. Tầng Tính toán & Biến đổi (Processing Layer): Apache Spark 4.2.0 thực thi các tác vụ xử lý phân tán: kiểm tra schema, làm sạch dữ liệu, tổng hợp chỉ số, kỹ nghệ đặc trưng và phân cụm KMeans MLlib.\n"
        "3. Tầng Lưu trữ Trung gian (Intermediate Storage): Dữ liệu sau khi làm sạch và phân tích được ghi ra định dạng Apache Parquet dạng cột (Columnar Storage) với khả năng nén cao Snappy.\n"
        "4. Tầng Dịch vụ Dữ liệu (Serving Layer): Apache Cassandra lưu trữ các kết quả tổng hợp phục vụ truy vấn thời gian thực với độ trễ mili-giây.\n"
        "5. Tầng Trực quan hóa (Presentation Layer): Ứng dụng Streamlit Dashboard truy vấn dữ liệu từ Cassandra và hiển thị biểu đồ trực quan."
    )

    doc.add_heading("4.2. Thiết kế Mô hình Dữ liệu NoSQL Cassandra (CQL Modeling)", level=2)
    doc.add_paragraph(
        "Để tuân thủ triệt để nguyên tắc không sử dụng `ALLOW FILTERING` khi quét lượng dữ liệu lớn, các bảng trong keyspace `pubg_analytics` "
        "được thiết kế tối ưu riêng biệt cho từng mẫu truy vấn của Dashboard:"
    )
    doc.add_paragraph(
        "1. Bảng `analytics_by_match_type`:\n"
        "   - Khóa chính: `PRIMARY KEY (match_type)`\n"
        "   - Mục đích: Phục vụ Trang 2 tra cứu nhanh các chỉ số tổng hợp theo chế độ chơi.\n"
        "2. Bảng `match_summary_by_id`:\n"
        "   - Khóa chính: `PRIMARY KEY (match_id)`\n"
        "   - Mục đích: Phục vụ Trang 4 tra cứu chi tiết trận đấu theo mã định danh `match_id`.\n"
        "3. Bảng `suspicious_records_by_run`:\n"
        "   - Khóa chính: `PRIMARY KEY (run_id, anomaly_score, player_id) WITH CLUSTERING ORDER BY (anomaly_score DESC, player_id ASC)`\n"
        "   - Mục đích: Khóa phân vùng là `run_id` và khóa sắp xếp là `anomaly_score DESC`. Thiết kế này cho phép phân trang và lấy Top-N người chơi có điểm bất thường cao nhất trực tiếp từ đĩa mà không cần sắp xếp lại trong bộ nhớ.\n"
        "4. Bảng `player_record_by_id`:\n"
        "   - Khóa chính: `PRIMARY KEY (player_id, match_id)`\n"
        "   - Mục đích: Tra cứu lịch sử thi đấu và lý do cảnh báo của một mã người chơi cụ thể."
    )

    doc.add_heading("4.3. Cơ chế Khả năng Phục hồi (Fault Resilience) và Persistent Fallback", level=2)
    doc.add_paragraph(
        "Trong môi trường máy tính cá nhân hoặc khi Docker chưa được khởi chạy, module `CassandraClient` được trang bị cơ chế tự động chuyển đổi an toàn (Transparent Fallback). "
        "Nếu cổng 9042 không phản hồi sau thời gian timeout, client tự động kích hoạt Local Persistent Storage (SQLite Mirror) lưu trữ cục bộ với cấu trúc bảng "
        "và kiểu dữ liệu tương đương 100% CQL Cassandra. Nhờ đó, ứng dụng Dashboard vẫn vận hành liên tục mà không bao giờ bị dừng đột ngột."
    )

    # =========================================================================
    # CHƯƠNG 5: MÔ HÌNH HỌC MÁY VÀ PHÁT HIỆN BẤT THƯỜNG
    # =========================================================================
    doc.add_heading("CHƯƠNG 5: MÔ HÌNH HỌC MÁY VÀ PHÁT HIỆN BẤT THƯỜNG", level=1)
    
    doc.add_heading("5.1. Kỹ nghệ Đặc trưng Hành vi Thi đấu (Feature Engineering)", level=2)
    doc.add_paragraph(
        "Từ 29 thuộc tính thô, nhóm tiến hành tính toán các chỉ số hành vi chuyên sâu:\n"
        "1. `totalDistance` = `walkDistance + rideDistance + swimDistance` (Tổng quãng đường di chuyển).\n"
        "2. `headshotRate` = `headshotKills / kills` khi kills > 0, ngược lại bằng 0.0 (Tỷ lệ bắn trúng đầu).\n"
        "3. `damagePerKill` = `damageDealt / kills` khi kills > 0 (Sát thương trung bình để hạ một mạng).\n"
        "4. `killsPerWalkKm` = `kills / ((walkDistance / 1000.0) + 0.001)` (Tỷ lệ mạng hạ gục trên mỗi kilomet đi bộ).\n"
        "5. Cờ vi phạm quy luật vật lý trò chơi (Domain Anti-Cheat Flags):\n"
        "   - `flag_teleport`: kills >= 5 nhưng walkDistance < 100.0m (Hạ gục nhiều người nhưng gần như đứng yên một chỗ).\n"
        "   - `flag_aimbot`: kills >= 8 và headshotRate >= 0.85 (Độ chính xác vào đầu vượt quá khả năng phản xạ con người).\n"
        "   - `flag_extreme_range`: longestKill > 1000.0m (Hạ gục ở khoảng cách vượt ngoài tầm render vật thể của động cơ game Unreal Engine 4).\n"
        "   - `flag_speed`: walkDistance > 13000.0m (Tốc độ đi bộ vượt quá giới hạn di chuyển tối đa trong thời lượng trận)."
    )

    doc.add_heading("5.2. Chuẩn hóa Vector và Huấn luyện Spark MLlib KMeans", level=2)
    doc.add_paragraph(
        "8 đặc trưng số học được đưa vào `VectorAssembler` và chuẩn hóa bằng `StandardScaler` (Z-score normalization). "
        "Mô hình KMeans với k = 4 cụm được huấn luyện trên cụm Spark. Kết quả đạt điểm Silhouette Score = 0.4665, "
        "cho thấy ranh giới các cụm hành vi rõ ràng và ổn định."
    )

    doc.add_heading("5.3. Tính toán Khoảng cách và Công thức Điểm Bất thường (Anomaly Score)", level=2)
    doc.add_paragraph(
        "Khoảng cách Euclidean từ vector đặc trưng tới tâm cụm tương ứng được tính toán hoàn toàn bằng Native Spark SQL Catalyst. "
        "Điểm bất thường (Anomaly Score, thang 0 - 100) được tính theo công thức kết hợp độ lệch thống kê và cờ vi phạm vật lý:\n\n"
        "   Score = (d_i / d_max) * 60 + flag_teleport * 25 + flag_aimbot * 25 + flag_extreme_range * 20 + flag_speed * 20\n\n"
        "Ngưỡng phân vị 99.5% của khoảng cách tương ứng với d_threshold = 6.6916. Các bản ghi có khoảng cách vượt ngưỡng hoặc kích hoạt "
        "bất kỳ cờ vi phạm vật lý nào sẽ được đánh dấu là `is_anomalous = True`."
    )

    doc.add_heading("5.4. Cơ chế Giải thích Lý do Cảnh báo (Explainable AI)", level=2)
    doc.add_paragraph(
        "Mỗi bản ghi bị đánh dấu đều đi kèm một chuỗi diễn giải định lượng cụ thể trong cột `reason`, ví dụ:\n"
        "  '[Aimbot] Tỷ lệ Headshot 85.7% (14 hạ gục) | [Độ lệch tâm cụm] Điểm khoảng cách: 22.51 (Sát thương 2,554.0)'\n"
        "Điều này giúp người quản trị hệ thống hiểu rõ cơ sở đánh dấu mà không phải xem xét các con số trừu tượng."
    )

    # Insert Figure 3 & 4
    fig3_path = PROJECT_ROOT / "reports" / "figures" / "anomaly_distribution.png"
    if fig3_path.exists():
        doc.add_paragraph()
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(fig3_path), width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run("Hình 4: Phân bố điểm bất thường (Anomaly Score) của các bản ghi bị đánh dấu")
        run_cap.font.italic = True
        run_cap.font.size = Pt(11)

    fig4_path = PROJECT_ROOT / "reports" / "figures" / "combat_scatter.png"
    if fig4_path.exists():
        doc.add_paragraph()
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(fig4_path), width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run("Hình 5: Biểu đồ phân tán Kills vs Quãng đường đi bộ phát hiện các ngoại lai dịch chuyển và aimbot")
        run_cap.font.italic = True
        run_cap.font.size = Pt(11)

    # =========================================================================
    # CHƯƠNG 6: THỰC NGHIỆM, KẾT QUẢ VÀ TRỰC QUAN HÓA
    # =========================================================================
    doc.add_heading("CHƯƠNG 6: THỰC NGHIỆM, KẾT QUẢ VÀ TRỰC QUAN HÓA", level=1)
    
    doc.add_heading("6.1. Thiết lập Môi trường và Kịch bản Thực nghiệm", level=2)
    doc.add_paragraph(
        "Thực nghiệm được tiến hành trên môi trường máy tính cá nhân Windows 11 với bộ xử lý AMD Ryzen, 16GB RAM, Java OpenJDK 17 và PySpark 4.2.0. "
        "Pipeline được thiết kế hỗ trợ hai kịch bản vận hành:\n"
        "- Chế độ Quick (`--mode quick`): Vận hành trên 94,428 bản ghi thuộc 1,000 trận đấu hoàn chỉnh. Dùng để phát triển, kiểm thử và demo bảo vệ trước hội đồng.\n"
        "- Chế độ Full (`--mode full`): Vận hành trên toàn bộ 4,446,966 bản ghi."
    )

    doc.add_heading("6.2. Kết quả Đo lường Hiệu năng Thực tế (Benchmark)", level=2)
    doc.add_paragraph(
        "Bảng thời gian thực thi thực tế từng giai đoạn được chương trình đo lường tự động (không sử dụng số liệu ước lượng):"
    )

    bench_data = [
        ("Giai đoạn Pipeline", "Công nghệ thực thi", "Thời gian (giây)", "Tỷ lệ thời gian"),
        ("1. Nạp dữ liệu CSV", "PySpark CSV Reader (Schema có sẵn)", "1.45 s", "2.3%"),
        ("2. Tiền xử lý & Kiểm tra chất lượng", "PySpark Filter & Validation", "5.94 s", "9.3%"),
        ("3. Phân tích thống kê & Tương quan", "Spark SQL Aggregations & Stat.corr", "5.25 s", "8.2%"),
        ("4. Kỹ nghệ đặc trưng hành vi", "VectorAssembler & StandardScaler", "2.73 s", "4.3%"),
        ("5. Huấn luyện KMeans & Anomaly Detection", "PySpark MLlib KMeans & Catalyst Calc", "22.96 s", "35.8%"),
        ("6. Ghi dữ liệu Parquet", "Spark Parquet Writer (Snappy)", "18.12 s", "28.3%"),
        ("7. Nạp dữ liệu Cassandra / Persistent Store", "Cassandra Client Batch Ingestion", "7.58 s", "11.8%"),
        ("TỔNG CỘNG TOÀN BỘ PIPELINE", "Hệ thống tích hợp hoàn chỉnh", "64.03 s", "100.0%")
    ]

    table_b = doc.add_table(rows=len(bench_data), cols=4)
    table_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(bench_data):
        for c_idx, val in enumerate(row):
            cell = table_b.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 80, 80, 100, 100)
            if r_idx == 0:
                set_cell_background(cell, "003366")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(bench_data) - 1:
                set_cell_background(cell, "EAECEE")
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.font.bold = True
            else:
                p = cell.paragraphs[0]
                p.runs[0].font.size = Pt(11)
                if c_idx in [2, 3]:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph()

    doc.add_heading("6.3. Phân tích Các Trường hợp Nghi vấn Điển hình (Case Studies)", level=2)
    doc.add_paragraph(
        "Mô hình đã phát hiện thành công 482 bản ghi bất thường (chiếm 0.510% tổng số người chơi). "
        "Dưới đây là một số trường hợp tiêu biểu trích xuất từ cơ sở dữ liệu:"
    )
    doc.add_paragraph(
        "1. Đối tượng `d0248b04b4ae5c` (duo-fpp): 14 mạng hạ gục, trong đó có tới 12 cú headshot (tỷ lệ 85.7%), tổng sát thương 2,554.0. Điểm khoảng cách tới tâm cụm đạt 22.51. Đây là trường hợp nghi vấn sử dụng công cụ tự ngắm bắn (Aimbot) cực kỳ rõ rệt.\n"
        "2. Đối tượng `f907f93f8f5698` (solo-fpp): 14 mạng hạ gục với 13 cú headshot (tỷ lệ 92.9% - gần như 100% đối thủ chết vì bị bắn vào đầu).\n"
        "3. Đối tượng `77b8be248d4137` (solo-fpp): Đạt điểm khoảng cách cực đại 104.61 (Anomaly Score: 60.0). Bản ghi này có mạng hạ gục nhưng quãng đường đi bộ bằng chính xác 0.0000m, phản ánh việc đứng yên tại chỗ bắn hạ đối phương từ xa hoặc dịch chuyển tức thời."
    )

    doc.add_heading("6.4. Giao diện Dashboard Trực quan hóa Streamlit", level=2)
    doc.add_paragraph(
        "Dashboard Streamlit (`dashboard/app.py`) được thiết kế đồng bộ với 4 trang tính năng trực quan:\n"
        "- Trang 1: Hiển thị các thẻ KPI thời gian thực (tổng bản ghi, số trận, số ca cảnh báo, thời gian pipeline), trạng thái kết nối Cassandra và phân bố chế độ chơi.\n"
        "- Trang 2: Bảng chỉ số chi tiết và biểu đồ so sánh sát thương, kills, quãng đường di chuyển theo chế độ chơi.\n"
        "- Trang 3: Danh sách các bản ghi nghi vấn với thanh trượt lọc Anomaly Score, lọc theo mức độ cảnh báo và biểu đồ phân tán Kills vs Khoảng cách.\n"
        "- Trang 4: Chức năng tra cứu chi tiết từng trận đấu theo `matchId` hoặc kiểm tra hồ sơ nghi vấn của người chơi theo `playerId`."
    )

    # =========================================================================
    # CHƯƠNG 7: THẢO LUẬN, GIỚI HẠN VÀ ĐẠO ĐỨC DỮ LIỆU
    # =========================================================================
    doc.add_heading("CHƯƠNG 7: THẢO LUẬN, GIỚI HẠN VÀ ĐẠO ĐỨC DỮ LIỆU", level=1)
    
    doc.add_heading("7.1. Phân biệt Giữa Thống kê Bất thường và Kết luận Gian lận", level=2)
    doc.add_paragraph(
        "Một trong những yêu cầu nghiêm ngặt nhất của đề tài là tính trung thực khoa học trong việc diễn giải kết quả. "
        "Cần nhấn mạnh rằng: 'Phát hiện thống kê bất thường' KHÔNG ĐỒNG NGHĨA với 'Khẳng định tài khoản đã gian lận'. "
        "Mô hình học máy không giám sát chỉ đóng vai trò phân loại và sàng lọc các bản ghi có hành vi lệch xa khỏi phân phối của người chơi bình thường. "
        "Đầu ra của hệ thống là danh sách các bản ghi cần trọng tài xem xét (Flagged for Review), giúp giảm tải 99.5% khối lượng công việc kiểm tra thủ công."
    )

    doc.add_heading("7.2. Thách thức Thiếu Nhãn Ground-Truth và Nguy cơ Dương tính Giả", level=2)
    doc.add_paragraph(
        "Do bộ dữ liệu công khai của PUBG không cung cấp nhãn xác nhận ban nick chính thức từ nhà phát hành, việc tính toán các độ đo có giám sát "
        "như Accuracy, Precision, Recall hay F1-Score là không hợp lệ về mặt phương pháp luận. Đề tài đã sử dụng đúng đắn độ đo Silhouette Score (0.4665) "
        "và phân vị khoảng cách để đánh giá mô hình.\n"
        "Nguy cơ dương tính giả (False Positives) vẫn có thể xảy ra khi một tuyển thủ chuyên nghiệp thi đấu ở bậc rank thấp hoặc gặp trận đấu 'thăng hoa' "
        "đạt chỉ số sát thương và headshot vượt trội. Vì vậy, hệ thống chống gian lận trong thực tế luôn cần kết hợp giữa phân tích dữ liệu lớn trên máy chủ "
        "với hệ thống giám sát tiến trình bộ nhớ trên máy khách."
    )

    # =========================================================================
    # CHƯƠNG 8: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN
    # =========================================================================
    doc.add_heading("CHƯƠNG 8: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", level=1)
    
    doc.add_paragraph(
        "Đề tài đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra cho môn học Nhập môn Big Data:\n"
        "1. Xây dựng hoàn chỉnh luồng xử lý Big Data từ khâu thu thập tự động bằng Kaggle CLI đến tiền xử lý và lưu trữ Parquet.\n"
        "2. Vận dụng hiệu quả năng lực tính toán phân tán của Apache Spark (PySpark DataFrame, Spark SQL, Spark MLlib).\n"
        "3. Ứng dụng thành công Apache Cassandra với mô hình Query-Driven Modeling tối ưu hóa truy vấn không cần ALLOW FILTERING.\n"
        "4. Xây dựng giải thuật phát hiện bất thường kết hợp giữa K-Means và các quy luật vật lý esports, cung cấp khả năng giải thích lý do rõ ràng.\n"
        "5. Phát triển Dashboard Streamlit trực quan, hỗ trợ kịch bản demo bảo vệ đề tài thuyết phục."
    )
    doc.add_paragraph(
        "Định hướng phát triển trong tương lai:\n"
        "- Tích hợp Apache Spark Streaming và Apache Kafka để xử lý luồng sự kiện trận đấu theo thời gian thực (Real-time Stream Processing).\n"
        "- Bổ sung mô hình học sâu (Deep Learning) phân tích chuỗi thời gian tọa độ di chuyển của người chơi để phát hiện hành vi bám tường (ESP) tinh vi hơn."
    )

    # =========================================================================
    # TÀI LIỆU THAM KHẢO
    # =========================================================================
    doc.add_heading("TÀI LIỆU THAM KHẢO", level=1)
    
    refs = [
        "[1] Kaggle Inc., 'PUBG Finish Placement Prediction Competition Dataset', 2018. [Online]. Available: https://www.kaggle.com/c/pubg-finish-placement-prediction",
        "[2] M. Zaharia, R. S. Xin, P. Wendell, T. Das, M. Armbrust, et al., 'Apache Spark: a unified engine for big data processing', Communications of the ACM, vol. 59, no. 11, pp. 56-65, 2016.",
        "[3] M. Armbrust, R. S. Xin, C. Lian, Y. Huai, et al., 'Spark SQL: Relational data processing in Spark', in Proc. ACM SIGMOD Int. Conf. on Management of Data, 2015, pp. 1383-1394.",
        "[4] X. Meng, J. Bradley, B. Yavuz, E. Sparks, et al., 'MLlib: Machine learning in Apache Spark', Journal of Machine Learning Research, vol. 17, no. 1, pp. 1235-1241, 2016.",
        "[5] A. Lakshman and P. Malik, 'Cassandra: a decentralized structured storage system', ACM SIGOPS Operating Systems Review, vol. 44, no. 2, pp. 35-40, 2010.",
        "[6] E. Hewitt and J. Carpenter, 'Cassandra: The Definitive Guide: Distributed Data at Web Scale', 3rd ed., O'Reilly Media, 2020.",
        "[7] A. R. Kang, J. Woo, J. Park, and H. K. Kim, 'Online game bot detection based on user behavioral analysis', in Proc. IEEE Conf. on Computational Intelligence in Games (CIG), 2013, pp. 1-8.",
        "[8] R. W. Ahmad, K. Salah, R. Jayaraman, et al., 'Blockchain and machine learning for anti-cheat and trust in esports', IEEE Access, vol. 10, pp. 15480-15494, 2022.",
        "[9] Streamlit Documentation, 'Streamlit: The fastest way to build and share data apps', 2024. [Online]. Available: https://docs.streamlit.io/"
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.add_run(r)

    # Save Word document
    output_docx = PROJECT_ROOT / "reports" / "report.docx"
    doc.save(str(output_docx))
    print(f">>> Đã tạo thành công báo cáo Word chuẩn học thuật tại: {output_docx} (Dung lượng: {output_docx.stat().st_size:,} bytes)")

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    create_report()
