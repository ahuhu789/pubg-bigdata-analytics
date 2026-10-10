# ĐỒ ÁN MÔN HỌC: NHẬP MÔN DỮ LIỆU LỚN (BIG DATA)

# ỨNG DỤNG APACHE SPARK VÀ CASSANDRA TRONG PHÂN TÍCH DỮ LIỆU TRẬN ĐẤU PUBG VÀ PHÁT HIỆN NGƯỜI CHƠI CÓ DẤU HIỆU GIAN LẬN TRONG THỂ THAO ĐIỆN TỬ

---

## 📌 1. Giới Thiệu Đề Tài

Trong các tựa game bắn súng sinh tồn nhiều người chơi quy mô lớn như **PlayerUnknown's Battlegrounds (PUBG)**, vấn nạn gian lận (cheat/hack: Aimbot, Teleport, Speed hack...) luôn là thách thức lớn nhất đe dọa sự công bằng của giải đấu esports.

Đồ án này xây dựng một hệ thống **Dữ liệu lớn (Big Data Pipeline)** hoàn chỉnh nhằm:
1. Thu thập dữ liệu thực tế hơn 4.44 triệu bản ghi từ Kaggle bằng **Kaggle CLI**.
2. Tiền xử lý, kiểm tra chất lượng và bảo toàn điểm cực trị bằng **Apache Spark (PySpark)**.
3. Phân tích thống kê trận đấu và mối liên hệ giữa các chỉ số bằng **Spark SQL**.
4. Phát hiện người chơi có dấu hiệu thống kê bất thường bằng **PySpark MLlib K-Means Clustering** kết hợp các cờ kiểm tra quy luật vật lý esports.
5. Lưu trữ phân tán theo mô hình tối ưu truy vấn trên **Apache Cassandra (NoSQL CQL)**.
6. Cung cấp giao diện trực quan hóa tương tác 4 trang bằng **Streamlit Dashboard**.

---

## 🏗️ 2. Kiến Trúc Hệ Thống (Big Data Architecture)

```text
Kaggle CLI (Cuộc thi chính thức: pubg-finish-placement-prediction)
    │
    ▼
PUBG Raw Dataset (train_V2.csv: 659.5 MB, 4.45M dòng)
    │
    ▼
Apache Spark / PySpark 4.2.0 (In-Memory Processing)
    ├── [1] Kiểm tra chất lượng & Tiền xử lý (Bảo toàn điểm cực trị)
    ├── [2] Phân tích thống kê trận đấu (GroupBy & Window Functions)
    ├── [3] Kỹ nghệ đặc trưng hành vi (VectorAssembler & StandardScaler)
    └── [4] Học máy phân cụm MLlib KMeans & Đo khoảng cách Native Catalyst
    │
    ▼
Apache Parquet (Columnar Storage nén Snappy tại data/processed/)
    │
    ▼
Apache Cassandra 4.1 (NoSQL Keyspace: pubg_analytics)
    ├── analytics_by_match_type (Khóa: match_type)
    ├── match_summary_by_id (Khóa: match_id)
    ├── suspicious_records_by_run (Khóa: run_id, Clustering: anomaly_score DESC)
    └── player_record_by_id (Khóa: player_id, match_id)
    │
    ▼
Streamlit Interactive Dashboard (Port: 8501)
    ├── Trang 1: Tổng quan dữ liệu & Trạng thái hạ tầng
    ├── Trang 2: Phân tích chuyên sâu trận đấu & Chế độ chơi
    ├── Trang 3: Danh sách cảnh báo Anomaly & Explainability
    └── Trang 4: Tra cứu chi tiết theo matchId / playerId
```

---

## 💻 3. Yêu Cầu Môi Trường & Công Cụ

- **Hệ điều hành:** Windows 10/11 (hoặc Linux/macOS).
- **Python:** Phiên bản 3.10 hoặc 3.11 (Khuyến nghị Python 3.11.x).
- **Java Runtime:** Java 8, 11 hoặc 17 (Khuyến nghị **Microsoft OpenJDK 17** hoặc Eclipse Temurin 17).
- **Hadoop Binaries (trên Windows):** `winutils.exe` và `hadoop.dll` (Đã được cấu hình tự động trong thư mục `tools/hadoop/bin`).
- **Kaggle CLI:** Đã cấu hình tệp xác thực `~/.kaggle/kaggle.json`.
- **Docker & Docker Compose (Tùy chọn):** Dùng để chạy cụm Apache Cassandra container. *(Nếu máy chưa cài Docker, hệ thống tự động kích hoạt chế độ Persistent Mirror tương đương 100% CQL để dashboard vẫn chạy mượt mà).*

---

## 🚀 4. Hướng Dẫn Cài Đặt & Chạy Dự Án

### Bước 1: Di chuyển vào thư mục dự án
```powershell
cd c:\Users\thanh\Desktop\klcn\pubg-bigdata-project
```

### Bước 2: Cài đặt các thư viện Python
```powershell
pip install -r requirements.txt
```

### Bước 3: Khởi động Apache Cassandra (Nếu có Docker)
Nếu máy bạn đã cài Docker Desktop:
```powershell
docker compose up -d
```
Kiểm tra trạng thái container:
```powershell
docker ps
```
*(Nếu không có Docker, bạn có thể bỏ qua bước này. Hệ thống sẽ tự kích hoạt chế độ lưu trữ dự phòng chuẩn hóa mà không gây lỗi).*

### Bước 4: Kiểm tra và tải dữ liệu từ Kaggle
```powershell
powershell scripts\download_data.ps1
```
Tập tin `train_V2.csv` (~660 MB) sẽ được tải vào thư mục `data/raw/`.

---

## ⚡ 5. Thực Thi Pipeline Big Data

Hệ thống hỗ trợ 2 chế độ vận hành:

### Chế độ 1: Quick Mode (Khuyến nghị cho Demo & Báo Cáo Bảo Vệ)
Sử dụng tập dữ liệu 94,428 bản ghi thuộc 1,000 trận đấu hoàn chỉnh để chạy demo nhanh trong khoảng **~60 giây**:
```powershell
powershell scripts\run_quick.ps1
# Hoặc chạy lệnh python trực tiếp:
python src\pipeline.py --mode quick
```

### Chế độ 2: Full Mode (Xử lý toàn bộ Big Data)
Xử lý trọn vẹn 4,446,966 bản ghi dữ liệu gốc:
```powershell
powershell scripts\run_full.ps1
# Hoặc:
python src\pipeline.py --mode full
```

### Bước 5: Khởi chạy Streamlit Dashboard
```powershell
streamlit run dashboard\app.py
```
Mở trình duyệt tại địa chỉ: `http://localhost:8501`.

---

## 📊 6. Kết Quả Thực Nghiệm Thực Tế (Benchmark)

Đo lường tự động trên chế độ `quick` (94,428 bản ghi / 1,000 trận đấu hoàn chỉnh):

| Giai đoạn Pipeline | Thời gian thực thi | Công nghệ |
| :--- | :---: | :--- |
| **Nạp dữ liệu CSV** | **1.45 s** | PySpark DataFrame Reader với Schema có sẵn |
| **Làm sạch & Kiểm tra** | **5.94 s** | PySpark Filter (Bảo toàn điểm cực trị) |
| **Phân tích trận đấu** | **5.25 s** | Spark SQL Aggregations & Window Functions |
| **Kỹ nghệ đặc trưng** | **2.73 s** | VectorAssembler & StandardScaler |
| **KMeans & Anomaly Detect** | **22.96 s** | PySpark MLlib (k=4, Silhouette: 0.4665) |
| **Ghi tệp Parquet** | **18.12 s** | Spark Parquet Columnar Storage (Snappy) |
| **Nạp CSDL Cassandra** | **7.58 s** | Cassandra Batch Ingestion |
| **TỔNG CỘNG PIPELINE** | **64.03 s (~1 phút 4 giây)** | **Hoàn thành 100%** |

### Thống kê Anomaly:
- **Ngưỡng phân vị khoảng cách (99.5%):** 6.6916 (Khoảng cách cực đại đo được: 104.61).
- **Số bản ghi có dấu hiệu bất thường phát hiện:** **482 bản ghi** (0.510% tổng số người chơi).
- **Các ca điển hình:**
  - `d0248b04b4ae5c`: 14 kills, 12 headshots (85.7% headshot rate), 2,554 sát thương (Nghi vấn Aimbot).
  - `77b8be248d4137`: 1 kill nhưng đi bộ 0.0m, khoảng cách tới tâm cụm 104.61 (Nghi vấn Teleport).

---

## 🎯 7. Kịch Bản Demo 5–7 Phút Trước Giảng Viên & Hội Đồng

Khi trình bày đồ án trước thầy cô, hãy thực hiện tuần tự theo kịch bản chuẩn sau:

1. **Phút 1: Giới thiệu đề tài & Dữ liệu**
   - Nêu vấn nạn hack/cheat trong PUBG esports và sự cần thiết của Big Data server-side.
   - Trình bày về bộ dữ liệu Kaggle 4.45M dòng và phương pháp lấy mẫu bảo toàn 1,000 trận đấu trọn vẹn (`train_quick.csv`).
2. **Phút 2: Trình bày Kiến trúc Hệ thống**
   - Mở slide số 5 (hoặc hình kiến trúc trong báo cáo) giải thích luồng: Kaggle CLI -> PySpark -> Parquet -> Cassandra -> Streamlit.
   - Giải thích vai trò của Spark (tính toán phân tán) và Cassandra (truy vấn NoSQL độ trễ thấp).
3. **Phút 3: Thực thi Pipeline Thực tế**
   - Mở PowerShell và chạy lệnh `python src\pipeline.py --mode quick`.
   - Chỉ cho giảng viên thấy các stage phân tán của Spark, quá trình huấn luyện KMeans và thời gian thực thi ~64 giây.
4. **Phút 4: Demo Dashboard - Trang 1 & Trang 2**
   - Mở Dashboard Streamlit (`http://localhost:8501`).
   - Trang 1: Xem các thẻ KPI, trạng thái hạ tầng Cassandra và tỷ trọng người chơi theo chế độ.
   - Trang 2: Xem các chế độ chơi đông nhất (squad-fpp: 421 trận) và ma trận tương quan giữa quãng đường đi bộ (+0.81) với tỷ lệ thắng.
5. **Phút 5: Demo Dashboard - Trang 3 & Trang 4 (Phát Hiện Bất Thường)**
   - Trang 3: Kéo thanh trượt Anomaly Score, chỉ ra 482 bản ghi nghi vấn và cột **Giải thích lý do (Explainability)**.
   - Phân tích ví dụ ca Aimbot (14 kills / 12 headshots) và ca Dịch chuyển (kills > 0 nhưng đi bộ 0m).
   - Trang 4: Tra cứu chi tiết một trận đấu theo `matchId`.
6. **Phút 6-7: Giải thích Giới hạn & Trả lời Phản biện**
   - Nhấn mạnh tính trung thực học thuật: Đây là "bản ghi có dấu hiệu thống kê bất thường trong một trận đấu", không phải kết luận ban nick vĩnh viễn vì thiếu nhãn ground-truth.
   - Trả lời các câu hỏi về partition key Cassandra và thuật toán KMeans.

---

## 📁 8. Cấu Trúc Mã Nguồn Dự Án

```text
pubg-bigdata-project/
├── README.md                      # Hướng dẫn chi tiết cài đặt và demo
├── requirements.txt               # Danh sách thư viện Python
├── .env.example                   # Biến môi trường mẫu
├── .gitignore                     # Bỏ qua tệp dữ liệu thô và rác hệ thống
├── docker-compose.yml             # Cấu hình container Apache Cassandra
├── data/
│   ├── raw/                       # Chứa train_V2.csv và train_quick.csv
│   └── processed/                 # Chứa các tệp Parquet và database
├── cassandra/
│   └── init.cql                   # Script khởi tạo Keyspace và 5 bảng NoSQL
├── src/
│   ├── config.py                  # Cấu hình đường dẫn, Java, SparkSession
│   ├── data_loader.py             # Nạp dữ liệu với PySpark Schema
│   ├── preprocessing.py           # Làm sạch dữ liệu, bảo toàn điểm cực trị
│   ├── match_analytics.py         # Phân tích thống kê trận đấu phân tán
│   ├── feature_engineering.py     # Kỹ nghệ 8 đặc trưng và cờ vi phạm vật lý
│   ├── anomaly_detection.py       # MLlib KMeans, Catalyst Distance & Explainability
│   ├── cassandra_client.py        # Client kết nối Cassandra có fallback
│   └── pipeline.py                # Điều phối toàn bộ Big Data Pipeline
├── dashboard/
│   └── app.py                     # Giao diện tương tác Streamlit 4 trang
├── scripts/
│   ├── download_data.ps1          # Script tải dữ liệu Kaggle CLI
│   ├── run_quick.ps1              # Chạy pipeline chế độ Quick
│   ├── run_full.ps1               # Chạy pipeline chế độ Full
│   ├── load_cassandra.py          # Nạp dữ liệu Parquet vào Cassandra
│   ├── generate_charts.py         # Xuất 5 biểu đồ chất lượng cao 300 DPI
│   └── verify_results.py          # Kiểm tra kết quả trong cơ sở dữ liệu
├── tests/
│   ├── test_preprocessing.py      # Unit test tiền xử lý và lọc rỗng
│   └── test_anomaly_detection.py  # Unit test cờ hành vi và fallback
└── reports/
    ├── report.docx                # Báo cáo học thuật Word hoàn chỉnh (32 trang)
    ├── slides.pptx                # Slide thuyết trình PowerPoint 12 trang
    ├── experiment_results.md      # Nhật ký số liệu thực nghiệm chi tiết
    ├── references.md              # Danh mục tài liệu tham khảo chuẩn IEEE
    └── figures/                   # 5 biểu đồ chất lượng cao đính kèm
```

---

## ⚖️ 9. Đạo Đức Dữ Liệu & Bản Quyền

- Bộ dữ liệu thuộc cuộc thi **PUBG Finish Placement Prediction** trên Kaggle, phục vụ mục đích nghiên cứu học thuật phi thương mại.
- Mọi kết quả phân tích phản ánh độ lệch thống kê của các bản ghi dữ liệu, không sử dụng cho mục đích phỉ báng hay quy kết cá nhân game thủ khi chưa có xác nhận từ nhà phát hành Krafton.
