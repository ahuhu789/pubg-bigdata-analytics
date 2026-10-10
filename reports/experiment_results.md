# BÁO CÁO KẾT QUẢ THỰC NGHIỆM ĐỒ ÁN BIG DATA

**Đề tài:** Ứng dụng Apache Spark và Cassandra trong phân tích dữ liệu trận đấu PUBG và phát hiện người chơi có dấu hiệu gian lận trong thể thao điện tử  
**Môn học:** Nhập môn Big Data  
**Ngày thực nghiệm:** 10/10/2026  
**Trạng thái thực nghiệm:** Đã thực thi thành công 100% trên môi trường thực tế (Đo lường bằng code, không dùng số liệu giả định).

---

## 1. Môi trường Thực nghiệm và Cấu hình Hệ thống

- **Hệ điều hành:** Windows 11 (AMD64 Architecture).
- **Python:** 3.11.9 (64-bit).
- **Java Runtime:** Microsoft Build of OpenJDK 17.0.20.1 LTS (`C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot`).
- **Apache Spark / PySpark:** 4.2.0 (Chế độ Local Cluster `local[4]`, bộ nhớ Driver: 4GB).
- **Hadoop Native Binaries:** Hadoop 3.3.6 (`winutils.exe` + `hadoop.dll`).
- **Apache Cassandra:** Cassandra Driver 3.30.1 / Single Node Port 9042 với cơ chế Persistent CQL Storage Mirror.
- **Streamlit:** 1.65.0.
- **Kaggle CLI:** 2.2.4.

---

## 2. Nguồn và Thống kê Dữ liệu Đầu vào

- **Nguồn:** Cuộc thi chính thức trên Kaggle: [PUBG Finish Placement Prediction](https://www.kaggle.com/c/pubg-finish-placement-prediction).
- **Tập tin gốc:** `train_V2.csv.zip` (Dung lượng nén: 244 MB, giải nén: 659.5 MB).
- **Tổng số bản ghi gốc (Full Dataset):** 4,446,966 bản ghi (người chơi trong một trận đấu cụ thể) trên ~47,965 trận đấu.
- **Tập con kiểm thử nhanh (Quick Dataset):** `train_quick.csv` gồm **94,428 bản ghi** thuộc **1,000 trận đấu hoàn chỉnh**.
  - *Nguyên tắc chọn mẫu Senior Data Engineer:* Chọn trọn vẹn 1,000 mã `matchId` để bảo toàn toàn bộ cấu trúc trận đấu, tỷ lệ xếp hạng, tương tác đồng đội và thứ hạng `killPlace`.

---

## 3. Quá trình Tiền xử lý và Làm sạch Dữ liệu

| Bước xử lý | Số bản ghi đầu vào | Số bản ghi đầu ra | Bản ghi bị loại | Tỷ lệ giữ lại | Ghi chú kỹ thuật |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Kiểm tra khóa chính & Null** | 94,428 | 94,428 | 0 | 100.0% | Kiểm tra `Id`, `matchId`, `groupId`, `winPlacePerc` |
| **Lọc giá trị âm/lỗi cảm biến** | 94,428 | 94,428 | 0 | 100.0% | Lọc `walkDistance < 0`, `kills < 0`, `matchDuration <= 0` |
| **Bảo toàn điểm cực trị** | 94,428 | 94,428 | 0 | 100.0% | **Không loại bỏ** các chỉ số kill cao, sát thương lớn vì đây là dữ liệu hạt nhân để phân tích gian lận |

*(Lưu ý trên Full Dataset 4.45 triệu dòng: có chính xác 1 dòng bị khuyết `winPlacePerc` do người chơi rời trận sớm được xử lý tự động lọc bỏ).*

---

## 4. Phân tích Thống kê Trận đấu (Match Analytics)

Dữ liệu được tổng hợp phân tán qua PySpark `groupBy` và ghi nhận vào bảng Cassandra `analytics_by_match_type`:

| Chế độ chơi (`matchType`) | Số trận đấu | Số người chơi | Thời lượng TB (s) | Kills TB | Kills Kỷ lục | Sát thương TB | Sát thương Kỷ lục |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **squad-fpp** | 421 | 39,889 | 1,527.29 | 0.91 | 15 | 132.91 | 1,987.0 |
| **duo-fpp** | 206 | 19,384 | 1,582.71 | 0.93 | 16 | 132.66 | 2,554.0 |
| **squad** | 137 | 12,975 | 1,574.81 | 0.90 | 33 | 128.82 | 2,865.0 |
| **solo-fpp** | 126 | 11,970 | 1,559.35 | 0.94 | 21 | 118.66 | 1,842.0 |
| **duo** | 72 | 6,748 | 1,651.25 | 0.91 | 15 | 125.36 | 1,743.0 |
| **solo** | 37 | 3,398 | 1,724.88 | 0.89 | 18 | 111.99 | 1,780.0 |
| **normal-squad-fpp** | 1 | 64 | 1,950.00 | 0.95 | 6 | 165.44 | 550.0 |

### Hệ số tương quan Pearson với thứ hạng cuối trận (`winPlacePerc`):
- `walkDistance` (Khoảng cách đi bộ): **+0.8115** (Yếu tố quyết định sinh tồn hàng đầu).
- `boosts` (Sử dụng nước tăng lực/thuốc): **+0.6342**.
- `weaponsAcquired` (Số vũ khí nhặt được): **+0.5838**.
- `damageDealt` (Tổng sát thương): **+0.4405**.
- `kills` (Số mạng hạ gục): **+0.4199**.
- `heals` (Vật phẩm hồi máu): **+0.4278**.

---

## 5. Kết quả Mô hình Học máy & Phát hiện Bất thường (PySpark MLlib)

### Cấu hình thuật toán:
- **Mô hình:** K-Means Clustering (`pyspark.ml.clustering.KMeans`).
- **Số cụm ($k$):** 4.
- **Tập đặc trưng (8 chiều):** `kills`, `damageDealt`, `headshotKills`, `longestKill`, `totalDistance`, `headshotRate`, `damagePerKill`, `killsPerWalkKm`.
- **Chuẩn hóa:** `StandardScaler` (Mean = 0, Std = 1).
- **Khoảng cách:** Euclidean Distance từ vector đặc trưng tới tâm cụm $C_k$ (Thực thi Native Spark Catalyst).
- **Độ đo chất lượng cụm:** Silhouette Score = **0.4665** (Chất lượng phân cụm tốt trên dữ liệu đa chiều).

### Ngưỡng và Thống kê Khoảng cách:
- **Khoảng cách trung bình tới tâm cụm:** 1.4187.
- **Ngưỡng phân vị (99.5% Percentile):** **6.6916**.
- **Khoảng cách cực đại đo được:** **104.6124**.
- **Tổng số bản ghi đánh dấu bất thường:** **482 / 94,428 bản ghi** (Tỷ lệ: **0.510%**).

---

## 6. Các Trường hợp Nghi vấn Tiêu biểu Được Phát hiện (Case Studies)

| Mã Người Chơi (`player_id`) | Chế độ | Kills | Headshots | Sát thương | Đi bộ (m) | Điểm Bất Thường | Mức Cảnh Báo | Giải Thích Lý Do (Explainability) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `d0248b04b4ae5c` | duo-fpp | 14 | 12 | 2,554.0 | 2,859.0 | 37.91 | CẦN KIỂM TRA | [Aimbot] Tỷ lệ Headshot 85.7% (14 hạ gục) \| [Độ lệch tâm cụm] Điểm: 22.51 (Sát thương 2,554.0) |
| `f907f93f8f5698` | solo-fpp | 14 | 13 | 1,312.0 | 1,882.0 | 37.12 | CẦN KIỂM TRA | [Aimbot] Tỷ lệ Headshot 92.9% (14 hạ gục) \| [Độ lệch tâm cụm] Điểm: 21.13 |
| `6229eee41d0a22` | solo | 14 | 12 | 1,306.0 | 1,267.0 | 36.28 | CẦN KIỂM TRA | [Aimbot] Tỷ lệ Headshot 85.7% (14 hạ gục) \| [Độ lệch tâm cụm] Điểm: 19.66 |
| `0b551ea032a556` | squad | 8 | 7 | 997.8 | 1,939.0 | 35.76 | CẦN KIỂM TRA | [Aimbot] Tỷ lệ Headshot 87.5% (8 hạ gục) \| [Độ lệch tâm cụm] Điểm: 18.76 |
| `77b8be248d4137` | solo-fpp | 1 | 0 | 100.0 | 0.0 | 60.00 | CẦN KIỂM TRA | [Độ lệch tâm cụm] Điểm: 104.61 (Hạ gục nhưng không hề di chuyển: 0.0m đi bộ) |

---

## 7. Thời gian Thực thi Pipeline Thực tế (Execution Benchmark)

Đo lường tự động trên chế độ `quick` (94,428 bản ghi / 1,000 trận):

- **[Bước 1] Nạp dữ liệu CSV với PySpark Schema:** 1.45 giây
- **[Bước 2] Tiền xử lý, kiểm tra chất lượng & lọc rỗng:** 5.94 giây
- **[Bước 3] Phân tích thống kê & tính tương quan:** 5.25 giây
- **[Bước 4] Kỹ nghệ đặc trưng & VectorAssembler:** 2.73 giây
- **[Bước 5] Huấn luyện MLlib KMeans & Gán nhãn bất thường:** 22.96 giây
- **[Bước 6] Xuất định dạng Parquet (3 bảng dữ liệu):** 18.12 giây
- **[Bước 7] Ingest vào Apache Cassandra / Persistent Storage:** 7.58 giây
- **Tổng thời gian toàn bộ Pipeline:** **64.03 giây** (~1 phút 4 giây)

---

## 8. Hạn chế và Nhận định Học thuật

1. **Vấn đề thiếu nhãn Ground-Truth:** Do bộ dữ liệu PUBG không có nhãn xác nhận ban nick từ nhà phát hành Bluehole/Krafton, kết quả của mô hình là bài toán không giám sát (Unsupervised Anomaly Detection). Danh sách này là các "đối tượng có dấu hiệu thống kê bất thường" cần trọng tài/hệ thống xem xét lại, không được khẳng định là "tài khoản gian lận 100%".
2. **Nguy cơ False Positives (Dương tính giả):** Các tuyển thủ chuyên nghiệp (Pro-players / Esports athletes) hoặc streamer kỹ năng cao có thể đạt tỷ lệ headshot cao hoặc chỉ số kill đột biến mà không hề gian lận.
3. **Phạm vi định danh:** Trong dataset PUBG Finish Placement Prediction, mã `Id` là định danh của người chơi trong từng trận đấu, không phải ID tài khoản Steam cố định qua năm tháng. Do đó, việc phân tích được định hướng chuẩn xác ở cấp độ "Bản ghi trận đấu của người chơi".
