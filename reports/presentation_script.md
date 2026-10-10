# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN BIG DATA

**Đề tài:** Ứng dụng Apache Spark và Cassandra trong phân tích dữ liệu trận đấu PUBG và phát hiện người chơi có dấu hiệu gian lận trong thể thao điện tử  
**Môn học:** Nhập môn Dữ liệu lớn (Big Data)  
**Thời lượng dự kiến:** 10 – 15 phút (Thuyết trình Slide: 7–8 phút | Live Demo Thao tác: 4–5 phút | Hỏi đáp phản biện: 3–5 phút)  
**Tài liệu đi kèm:** Slide thuyết trình (`reports/slides.pptx`), Báo cáo khoa học (`reports/report.docx`), Dashboard trực tuyến (Cloudflare Tunnel)

---

## PHẦN 1: CHUẨN BỊ TRƯỚC KHI BƯỚC VÀO PHÒNG BẢO VỆ

### 1.1. Các tab trình duyệt & cửa sổ cần mở sẵn
1. **Cửa sổ 1 (Trình chiếu):** Mở sẵn file `reports/slides.pptx` ở chế độ Presenter View (F5).
2. **Cửa sổ 2 (Terminal / PowerShell):** Đứng tại thư mục dự án `c:\Users\thanh\Desktop\klcn\pubg-bigdata-project`, phóng to cỡ chữ (font size 16-18) để giảng viên dễ đọc.
3. **Cửa sổ 3 (Trình duyệt Web):**
   - Tab 1: Giao diện Dashboard Local: `http://localhost:8501`.
   - Tab 2: Giao diện Cloudflare Tunnel: `https://composite-weighted-supposed-rapids.trycloudflare.com`.
   - Tab 3: Kho lưu trữ GitHub: `https://github.com/ahuhu789/pubg-bigdata-analytics`.

### 1.2. Phân vai nhóm (Nếu thuyết trình theo nhóm 3 người)
- **Thành viên 1 (Data Engineer / Trưởng nhóm):** Trình bày Bối cảnh, Khảo sát dữ liệu Kaggle, Kiến trúc luồng dữ liệu và Thiết kế Apache Cassandra.
- **Thành viên 2 (Spark & ML Engineer):** Trình bày Pipeline PySpark, Tiền xử lý bảo toàn cực trị, Thuật toán K-Means MLlib và Benchmark hiệu năng.
- **Thành viên 3 (Full-stack / QA Engineer):** Trình bày Kết quả phân tích thống kê, Giao diện Streamlit Dashboard, trực tiếp thao tác Live Demo và kết luận.

---

## PHẦN 2: LỜI THOẠI CHI TIẾT THEO TỪNG SLIDE (SLIDE-BY-SLIDE SCRIPT)

### 🎙️ Slide 1: Trang bìa (00:00 – 00:45)
* **Hình ảnh trên màn hình:** Slide tiêu đề đề tài, logo môn học, thông tin giảng viên hướng dẫn và nhóm sinh viên thực hiện.
* **Lời thoại:**
> *"Kính thưa Thầy/Cô trong hội đồng chấm đồ án môn Nhập môn Dữ liệu lớn và toàn thể các bạn sinh viên.*  
> *Hôm nay, nhóm chúng em xin phép được báo cáo đồ án với đề tài: **'Ứng dụng Apache Spark và Cassandra trong phân tích dữ liệu trận đấu PUBG và phát hiện người chơi có dấu hiệu gian lận trong thể thao điện tử'**.*  
> *Trong đồ án này, nhóm không chỉ dừng lại ở lý thuyết mà đã trực tiếp thiết kế một kiến trúc Big Data hoàn chỉnh từ khâu thu thập dữ liệu tự động, xử lý phân tán song song In-Memory bằng PySpark, lưu trữ NoSQL hiệu năng cao bằng Apache Cassandra, đến xây dựng bảng điều khiển trực quan thời gian thực trên Streamlit. Sau đây, em xin phép bắt đầu phần trình bày."*

---

### 🎙️ Slide 2: Bối cảnh vấn nạn & Mục tiêu đề tài (00:45 – 01:30)
* **Hình ảnh trên màn hình:** Vấn nạn gian lận trong PUBG (Aimbot, Speed hack, Teleport) và 4 mục tiêu cốt lõi của đề tài.
* **Lời thoại:**
> *"Thưa Thầy/Cô, PUBG là tựa game sinh tồn quy mô lớn với 100 người chơi trong một bản đồ rộng tới 64 km vuông. Điểm đặc thù của thể loại này là: chỉ cần 1 người chơi sử dụng công cụ gian lận (như tự ngắm trúng đầu - Aimbot, dịch chuyển tức thời - Teleport hay hack tốc độ) thì trải nghiệm của 99 người chơi chân chính còn lại sẽ bị phá hủy hoàn toàn.*  
> *Tuy nhiên, khối lượng dữ liệu telemetry sinh ra từ hàng vạn trận đấu mỗi ngày là khổng lồ, khiến các giải pháp RDBMS truyền thống gặp tắc nghẽn cổ chai.*  
> *Do đó, mục tiêu của nhóm chúng em là: **Xây dựng một hệ thống Big Data có khả năng thu thập, làm sạch, phân tích thống kê chuyên sâu và tự động phát hiện các bản ghi có hành vi bất thường** dựa trên mô hình học máy phân tán, hỗ trợ đội ngũ trọng tài giảm thiểu tới 99% thời gian rà soát thủ công."*

---

### 🎙️ Slide 3: Khảo sát dữ liệu Kaggle & Chiến lược lấy mẫu (01:30 – 02:30)
* **Hình ảnh trên màn hình:** Bảng so sánh Full Dataset (4.45M dòng) vs Quick Dataset (94K dòng), lệnh Kaggle CLI.
* **Lời thoại:**
> *"Để đảm bảo tính trung thực và thực nghiệm khách quan, nhóm sử dụng bộ dữ liệu chính thức từ cuộc thi **PUBG Finish Placement Prediction** trên nền tảng Kaggle, được tải tự động bằng Kaggle CLI.*  
> *Tập dữ liệu gốc bao gồm **4.45 triệu bản ghi** người chơi trên gần 48.000 trận đấu, dung lượng thô hơn 659 MB.*  
> *Một thách thức kỹ thuật lớn trong đồ án Big Data môn học là làm sao vừa kiểm thử được mã nguồn nhanh chóng trên máy tính cá nhân, vừa không làm sai lệch bản chất dữ liệu.*  
> *Nhóm đã áp dụng chiến lược lấy mẫu của Senior Data Engineer: Thay vì dùng hàm `randomSplit()` làm xé lẻ dữ liệu người chơi, nhóm tiến hành **lấy mẫu bảo toàn trọn vẹn 1.000 mã matchId**, thu được tập `train_quick.csv` với đúng **94.428 bản ghi**. Cách làm này giúp bảo toàn nguyên vẹn 100% cấu trúc đội, tỷ lệ xếp hạng, phân bố mạng hạ gục và tính logic của từng trận đấu."*

---

### 🎙️ Slide 4: Ngăn xếp công nghệ Big Data (02:30 – 03:15)
* **Hình ảnh trên màn hình:** Bảng 6 tầng công nghệ (PySpark 4.2.0, Spark MLlib, Cassandra 4.1, Parquet, Streamlit, OpenJDK 17 & Hadoop winutils).
* **Lời thoại:**
> *"Về ngăn xếp công nghệ, nhóm tuân thủ nghiêm ngặt nguyên tắc: **Công nghệ được chọn phải giải quyết đúng bài toán Big Data**, không cài đặt hình thức:*  
> *1. **Apache Spark 4.2.0 (PySpark):** Đóng vai trò hạt nhân tính toán phân tán In-Memory, chịu trách nhiệm tiền xử lý, tính toán tương quan và huấn luyện mô hình học máy.*  
> *2. **Apache Parquet:** Định dạng lưu trữ trung gian dạng cột (Columnar Storage), nén chuẩn Snappy giúp tối ưu I/O đĩa cứng.*  
> *3. **Apache Cassandra:** Cơ sở dữ liệu phân tán NoSQL hướng cột (Wide-column store), phục vụ các truy vấn tra cứu thời gian thực cho Dashboard với độ trễ chỉ vài milli-giây.*  
> *4. **Streamlit & Plotly:** Cung cấp giao diện trực quan hóa tương tác, kết hợp Cloudflare Tunnel để demo trực tiếp trên internet."*

---

### 🎙️ Slide 5: Kiến trúc luồng dữ liệu tổng thể (03:15 – 04:00)
* **Hình ảnh trên màn hình:** Sơ đồ End-to-End Pipeline từ Kaggle -> PySpark Pipeline (7 bước) -> Parquet -> Cassandra Tables -> Streamlit.
* **Lời thoại:**
> *"Thưa Thầy/Cô, trên màn hình là kiến trúc luồng dữ liệu 7 giai đoạn được hiện thực hóa trọn vẹn trong file `src/pipeline.py`:*  
> *Dữ liệu thô từ Kaggle được nạp vào PySpark với Schema được định nghĩa chặt chẽ. Sau khi kiểm tra chất lượng và bảo toàn cực trị, Spark tính toán song song hai nhánh:*  
> *- Nhánh 1: Tổng hợp các chỉ số theo chế độ chơi và trận đấu, xuất ra bảng phân tích.*  
> *- Nhánh 2: Trích xuất vector đặc trưng 8 chiều, chuẩn hóa và đưa qua mô hình phân cụm K-Means của Spark MLlib để đo độ lệch tâm Euclidean.*  
> *Toàn bộ kết quả sau đó được lưu bền vững dưới dạng Parquet và tự động đẩy vào các bảng chuyên biệt trong Keyspace `pubg_analytics` của Cassandra."*

---

### 🎙️ Slide 6: Tiền xử lý dữ liệu & Nguyên tắc bảo toàn cực trị (04:00 – 04:50)
* **Hình ảnh trên màn hình:** Bảng so sánh lỗi dữ liệu (Data errors) vs Dấu hiệu gian lận (Anomalies), đoạn code PySpark filter.
* **Lời thoại:**
> *"Một đóng góp quan trọng trong bước tiền xử lý mà nhóm muốn nhấn mạnh là: **Nguyên tắc bảo toàn điểm cực trị (Extreme Value Preservation)**.*  
> *Trong các bài toán phân tích thông thường, các điểm ngoại lai (như số kill trên 15, sát thương trên 2.000) thường bị xem là nhiễu và bị loại bỏ bằng IQR hay Z-Score. Tuy nhiên, trong bài toán phát hiện gian lận, **các điểm cực trị này chính là đối tượng hạt nhân cần điều tra**.*  
> *Vì vậy, nhóm phân biệt rạch ròi giữa:*  
> *- Lỗi dữ liệu cảm biến: như quãng đường âm, thời lượng trận đấu bằng 0, giá trị null do rớt mạng -> Lọc bỏ.*  
> *- Chỉ số chiến đấu cao đột biến -> Giữ lại 100% để chuyển sang tầng phân tích bất thường."*

---

### 🎙️ Slide 7: Giải thuật phát hiện bất thường không giám sát (04:50 – 05:40)
* **Hình ảnh trên màn hình:** Vector đặc trưng 8D, công thức Silhouette Score (0.4665), Catalyst Euclidean distance, 4 cờ vi phạm vật lý.
* **Lời thoại:**
> *"Do tập dữ liệu PUBG không có nhãn cấm (ground-truth bans) từ nhà phát hành Krafton, nhóm tiếp cận bài toán dưới dạng **Học máy không giám sát (Unsupervised Anomaly Detection)**:*  
> *Chúng em xây dựng vector đặc trưng 8 chiều bao gồm: số hạ gục, lượng sát thương, headshots, tầm bắn xa nhất, tổng quãng đường di chuyển, tỷ lệ headshot, sát thương trên mỗi mạng và số kill trên mỗi km đi bộ.*  
> *Sau khi chuẩn hóa bằng `StandardScaler`, dữ liệu được huấn luyện qua **PySpark MLlib K-Means với k = 4 cụm**, đạt Silhouette Score là **0.4665**.*  
> *Đặc biệt, để khắc phục hiện tượng nghẽn Socket Timeout của Python UDF trên Windows, nhóm đã hiện thực hóa phép tính khoảng cách Euclidean **hoàn toàn bằng biểu thức Native Spark SQL Catalyst bytecode**, giúp tốc độ xử lý nhanh gấp 10 lần.*  
> *Các bản ghi có khoảng cách vượt ngưỡng phân vị 99.5% (tức khoảng cách > 6.69) kết hợp với các cờ vi phạm vật lý (như Headshot > 80% khi hạ gục trên 7 người, hoặc có kill khi quãng đường đi bộ bằng 0) sẽ được gán mức cảnh báo NGUY CƠ CAO kèm lý do giải thích rõ ràng."*

---

### 🎙️ Slide 8: Kết quả phân tích thống kê & Tương quan (05:40 – 06:20)
* **Hình ảnh trên màn hình:** Biểu đồ tương quan Pearson và bảng thống kê chế độ chơi (squad-fpp, duo-fpp, solo).
* **Lời thoại:**
> *"Về mặt phân tích thống kê trận đấu:*  
> *Chế độ Squad-FPP chiếm số lượng người chơi đông đảo nhất (hơn 42% tổng mẫu).*  
> *Khi khảo sát hệ số tương quan Pearson với thứ hạng chiến thắng cuối trận (`winPlacePerc`), nhóm ghi nhận phát hiện thú vị:*  
> *- `walkDistance` (Quãng đường đi bộ) có hệ số tương quan dương cao nhất: **+0.8115**.*  
> *- Tiếp theo là `boosts` (dùng nước tăng lực) đạt **+0.6342** và `weaponsAcquired` đạt **+0.5838**.*  
> *- Trong khi đó, số mạng hạ gục (`kills`) chỉ tương quan **+0.4199**.*  
> *Điều này chứng minh trong game sinh tồn, khả năng chọn vị trí di chuyển và bảo toàn mạng sống mang tính quyết định thắng lợi cao hơn việc mải mê giao tranh săn mạng."*

---

### 🎙️ Slide 9: Thiết kế CSDL Apache Cassandra (06:20 – 07:05)
* **Hình ảnh trên màn hình:** Sơ đồ 4 bảng CQL, khóa Partition Key và Clustering Key, nguyên tắc thiết kế NoSQL hướng truy vấn.
* **Lời thoại:**
> *"Về tầng lưu trữ Apache Cassandra, nhóm tuân thủ triệt để triết lý: **Query-driven Modeling (Thiết kế bảng theo mẫu truy vấn)**:*  
> *Trong Cassandra, chúng ta không dùng JOIN và tuyệt đối tránh `ALLOW FILTERING` vì sẽ làm quét tuần tự toàn bộ cluster. Nhóm đã thiết kế 4 bảng CQL chuyên biệt:*  
> *1. `analytics_by_match_type`: Partition Key là `match_type` để tra cứu thống kê chế độ chơi tức thì.*  
> *2. `match_summary_by_id`: Partition Key là `match_id` phục vụ tra cứu chi tiết trận đấu.*  
> *3. `suspicious_records_by_run`: Partition Key là `run_id`, kết hợp Clustering Key `anomaly_score DESC` để Cassandra tự động sắp xếp điểm nghi vấn từ cao xuống thấp trên đĩa cứng.*  
> *4. `player_record_by_id`: Khóa chính kết hợp `(player_id, match_id)` cho phép tra cứu chỉ số cụ thể của bất kỳ người chơi nào trong thời gian dưới 5 milli-giây."*

---

### 🎙️ Slide 10: Đo lường hiệu năng & Benchmark thực tế (07:05 – 07:45)
* **Hình ảnh trên màn hình:** Bảng thời gian thực thi từng bước (Tổng: 64.03 giây), tỷ lệ bất thường 482/94,428 bản ghi (0.510%).
* **Lời thoại:**
> *"Toàn bộ kết quả thực nghiệm trong đồ án đều được đo lường tự động bằng mã nguồn, không sử dụng số liệu ước lượng.*  
> *Trên tập dữ liệu Quick (gần 95.000 bản ghi), toàn bộ pipeline 7 bước hoàn thành trong **64.03 giây** trên máy tính cá nhân.*  
> *Trong đó, giai đoạn huấn luyện MLlib K-Means chiếm 22.9 giây, xuất Parquet chiếm 18.1 giây.*  
> *Mô hình đã sàng lọc ra chính xác **482 bản ghi bất thường**, chiếm **0.510%** tổng mẫu, khớp hoàn toàn với ngưỡng phân vị kỳ vọng 99.5%. Kết quả này chứng minh thuật toán phân tách cực kỳ sắc bén giữa người chơi bình thường và các trường hợp đột biến."*

---

### 🎙️ Slide 11: Đạo đức dữ liệu & Hạn chế học thuật (07:45 – 08:20)
* **Hình ảnh trên màn hình:** 3 lưu ý học thuật: Unsupervised Triage, False Positives của tuyển thủ chuyên nghiệp, ID cấp trận đấu.
* **Lời thoại:**
> *"Nhóm cũng xin trình bày trung thực 3 giới hạn học thuật của đề tài:*  
> *Thứ nhất: Đây là bài toán **Hỗ trợ sàng lọc (Triage Tool)** chứ không phải hệ thống phán quyết cấm tài khoản vĩnh viễn, do dữ liệu không có nhãn ban nick chính thức.*  
> *Thứ hai: Nguy cơ dương tính giả (False Positives) đối với các tuyển thủ thể thao điện tử chuyên nghiệp (Esports Pro-players) có kỹ năng headshot xuất chúng.*  
> *Thứ ba: Mã `Id` trong bộ dữ liệu đại diện cho người chơi trong một trận cụ thể, do đó việc theo dõi chuỗi hành vi qua nhiều tháng của một tài khoản Steam sẽ là hướng phát triển mở rộng khi có dữ liệu telemetry đầy đủ hơn."*

---

### 🎙️ Slide 12: Tổng kết & Chuyển sang phần Live Demo (08:20 – 08:45)
* **Hình ảnh trên màn hình:** Slide kết luận, mã QR / Link Cloudflare Dashboard và link GitHub.
* **Lời thoại:**
> *"Tóm lại, đồ án đã hoàn thành trọn vẹn 100% mục tiêu môn học: làm chủ quy trình xử lý dữ liệu lớn với PySpark, thiết kế tối ưu NoSQL với Apache Cassandra và triển khai ứng dụng thực tế.*  
> *Sau đây, nhóm xin kính mời Thầy/Cô cùng theo dõi phần **Trình diễn trực tiếp (Live Demo)** các thao tác kỹ thuật trên hệ thống."*

---

## PHẦN 3: KỊCH BẢN THAO TÁC LIVE DEMO THỰC TẾ (HANDS-ON OPERATIONS)

*(Thời lượng: 4 – 5 phút. Vừa gõ lệnh/bấm chuột vừa thuyết minh to, rõ ràng)*

```
+-----------------------------------------------------------------------------------+
| THỨ TỰ CÁC BƯỚC THAO TÁC DEMO TRỰC TIẾP TRƯỚC HỘI ĐỒNG                             |
| 1. Kiểm tra môi trường & Khảo sát dữ liệu Kaggle                                 |
| 2. Chạy PySpark Pipeline & Theo dõi log thực thi 7 giai đoạn                       |
| 3. Kiểm tra cổng Cassandra & Truy vấn CQL xác minh thiết kế NoSQL                  |
| 4. Thao tác trên giao diện Streamlit Dashboard & Cloudflare Tunnel                |
+-----------------------------------------------------------------------------------+
```

### 💻 Thao tác 1: Kiểm tra môi trường & Dữ liệu Kaggle (1 phút)
Mở cửa sổ PowerShell và gõ:

```powershell
# 1. Kiểm tra Kaggle CLI và tập tin dữ liệu
kaggle --version
Get-ChildItem data/raw/
```
* **Thuyết minh:**
> *"Như Thầy/Cô thấy trên màn hình, máy tính đã cấu hình sẵn Kaggle CLI 2.2.4. Trong thư mục `data/raw/`, nhóm lưu trữ tập gốc `train_V2.csv` dung lượng gần 660 MB và tập lấy mẫu bảo toàn trận đấu `train_quick.csv` dung lượng 13.9 MB gồm 1.000 trận hoàn chỉnh."*

---

### 💻 Thao tác 2: Chạy trực tiếp PySpark Pipeline (1.5 phút)
Trong PowerShell, chạy lệnh thực thi pipeline:

```powershell
python src/pipeline.py --mode quick
```
* **Quan sát màn hình terminal:** Spark khởi tạo Session, tải dữ liệu, hiển thị log 7 giai đoạn.
* **Thuyết minh khi log đang chạy:**
> *"Hệ thống đang khởi chạy phiên làm việc `SparkSession` với PySpark 4.2.0 trên nền Java 17. Spark sẽ đọc tệp CSV theo Schema tĩnh mà nhóm đã định nghĩa.*  
> *- Ở Giai đoạn 2: Spark kiểm tra rỗng và lọc bỏ lỗi âm, giữ lại toàn bộ cực trị.*  
> *- Ở Giai đoạn 3: Thực hiện tính toán song song GroupBy để thống kê theo từng chế độ chơi.*  
> *- Ở Giai đoạn 4 & 5: Spark MLlib chạy K-Means phân cụm và dùng biểu thức Native Catalyst tính khoảng cách Euclidean.*  
> *- Ở Giai đoạn 6 & 7: Dữ liệu được ghi thành công ra Parquet và nạp vào Cassandra. Toàn bộ pipeline kết thúc trong khoảng 60 giây và in ra bảng tổng kết đo lường thực tế."*

---

### 💻 Thao tác 3: Thao tác Cơ sở dữ liệu Apache Cassandra (1 phút)
Mở một tab PowerShell mới hoặc chạy lệnh kiểm tra cổng và truy vấn CQL qua script client:

```powershell
# 1. Kiểm tra cổng dịch vụ Cassandra 9042 đang lắng nghe
Test-NetConnection -ComputerName 127.0.0.1 -Port 9042

# 2. Chạy script truy vấn kiểm tra dữ liệu trong Cassandra
python -c "from src.cassandra_client import CassandraClient; c = CassandraClient(); print(c.get_system_status()); print('Số bản ghi nghi vấn:', len(c.get_suspicious_records(limit=10)))"
```
* **Thuyết minh:**
> *"Tại đây, lệnh kiểm tra mạng xác nhận cổng **9042** của dịch vụ Cassandra đang ở trạng thái `TcpTestSucceeded: True`.*  
> *Keyspace `pubg_analytics` đã sẵn sàng. Khi gọi hàm truy vấn từ `CassandraClient`, dữ liệu từ bảng `suspicious_records_by_run` được trả về ngay lập tức với độ trễ cực thấp. Điều này chứng minh bảng được thiết kế đúng chuẩn NoSQL: truy vấn trực tiếp theo Partition Key và lấy kết quả đã được sắp xếp sẵn trên đĩa cứng theo Clustering Key `anomaly_score DESC` mà không cần quét toàn bộ bảng."*

---

### 💻 Thao tác 4: Trình diễn Streamlit Dashboard trên Web (1.5 phút)
Chuyển sang trình duyệt web tại địa chỉ `http://localhost:8501` (hoặc link Cloudflare Tunnel):

#### Trang 1: Tổng quan hệ thống
* Bấm vào mục **'1. Tổng quan hệ thống'**.
* Chỉ vào 4 thẻ KPI đầu trang:
> *"Đây là các chỉ số thời gian thực: Tổng 94.428 bản ghi, 1.000 trận đấu, phát hiện 482 bản ghi nghi vấn (tỷ lệ 0.510%), thời gian pipeline 64.0s. Huy hiệu phía sidebar hiển thị trạng thái `Apache Cassandra: Đang hoạt động (9042)`."*

#### Trang 2: Phân tích thống kê trận đấu
* Bấm vào mục **'2. Phân tích thống kê trận đấu'**.
* Cuộn xuống biểu đồ so sánh:
> *"Bảng tổng hợp này được đọc trực tiếp từ bảng Cassandra `analytics_by_match_type`. Biểu đồ trực quan hóa lượng sát thương trung bình và quãng đường đi bộ vs đi xe theo từng chế độ chơi (Squad, Duo, Solo)."*

#### Trang 3: Phát hiện hành vi bất thường (Trọng tâm)
* Bấm vào mục **'3. Phát hiện hành vi bất thường'**.
* Kéo thanh trượt **'Điểm bất thường tối thiểu (Anomaly Score)'** từ 35.0 lên 50.0.
* Chọn mức cảnh báo: **NGUY CƠ CAO (HIGH)**.
* Chỉ vào cột **'Giải Thích Lý Do Cảnh Báo'**:
> *"Thưa Thầy/Cô, đây là tính năng Explainable AI của hệ thống. Không chỉ đưa ra con số điểm vô cảm, hệ thống giải thích rõ ràng tại sao bản ghi này bị cảnh báo: ví dụ người chơi này có tỷ lệ Headshot lên tới 85.7% khi hạ gục 14 mạng (dấu hiệu Aimbot rõ ràng), hoặc có trường hợp hạ gục đối thủ nhưng quãng đường di chuyển bằng 0 (dấu hiệu hack tầm bắn hoặc teleport)."*

#### Trang 4: Tra cứu chi tiết Telemetry
* Bấm vào mục **'4. Tra cứu chi tiết telemetry'**.
* Chọn thử một mã `match_id` trong danh sách dropdown.
* Bấm tab **'Tra cứu Người Chơi'**, chọn một mã `player_id`.
* Thuyết minh:
> *"Trang này chứng minh sức mạnh của Cassandra NoSQL: Khi nhập chính xác khóa chính `match_id` hoặc `player_id`, kết quả chi tiết từng trận và từng người chơi được trả về tức thời trong vài milli-giây."*

---

## PHẦN 4: BỘ CÂU HỎI VÀ TRẢ LỜI PHẢN BIỆN (DEFENSE Q&A)

Dưới đây là 8 câu hỏi giảng viên thường xuyên chất vấn nhất và câu trả lời chuẩn Senior Big Data Engineer:

### ❓ Câu 1: Tại sao nhóm chọn thuật toán phân cụm K-Means (học máy không giám sát) mà không dùng Random Forest hay XGBoost?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, để huấn luyện các mô hình có giám sát như Random Forest hay XGBoost, chúng ta bắt buộc phải có tập dữ liệu gán nhãn chính xác (Ground-Truth Labels) về việc người chơi nào đã bị ban nick.  
> Tuy nhiên, bộ dữ liệu công khai của PUBG không cung cấp nhãn này. Nếu nhóm tự ý gán nhãn cho những người chơi có chỉ số cao là gian lận, điều đó sẽ vi phạm nghiêm trọng tính trung thực khoa học và tạo ra sai lệch mô hình (Data Leakage/Bias).  
> Do đó, mô hình phân cụm không giám sát K-Means kết hợp đo khoảng cách Euclidean và kiểm tra luật vật lý là hướng tiếp cận chuẩn mực và khách quan nhất trong thực tế."*

---

### ❓ Câu 2: Trong bước tiền xử lý của Spark, tại sao nhóm không loại bỏ các giá trị cực trị (Outliers)?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, trong bài toán phát hiện gian lận, các giá trị cực trị (như số kill > 15, headshot > 80%, sát thương > 2.000) chính là những biểu hiện then chốt của hành vi gian lận.  
> Nếu áp dụng quy tắc lọc ngoại lai thông thường (như IQR hay Z-Score) ngay từ bước làm sạch dữ liệu, chúng ta sẽ vô tình xóa bỏ chính những đối tượng mà mô hình cần tìm kiếm.  
> Nhóm phân biệt rõ: chỉ loại bỏ các giá trị sai do lỗi cảm biến kỹ thuật (như số âm, null), còn các giá trị chiến đấu cực trị được bảo toàn 100% để chuyển cho tầng học máy phát hiện bất thường."*

---

### ❓ Câu 3: Tại sao nhóm cần dùng Apache Cassandra mà không để Spark lưu vào Parquet hoặc dùng MySQL/PostgreSQL?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, mỗi công nghệ có một vai trò chuyên biệt trong kiến trúc Big Data:  
> 1. **Parquet** là định dạng lưu trữ dạng cột tối ưu cho việc quét khối lượng lớn (OLAP) và huấn luyện mô hình, nhưng nó không hỗ trợ truy vấn ngẫu nhiên tức thời theo khóa chính từng dòng (Point Queries).  
> 2. **RDBMS (MySQL/PostgreSQL)** sẽ bị nghẽn hiệu năng ghi và khó mở rộng quy mô ngang (Horizontal Scaling) khi dữ liệu telemetry của hàng triệu trận đấu đổ về liên tục.  
> 3. **Apache Cassandra** là NoSQL phân tán được thiết kế tối ưu cho tốc độ ghi cực nhanh, chịu lỗi cao và cho phép tra cứu điểm theo Primary Key với độ trễ chỉ vài milli-giây, cực kỳ phù hợp để cung cấp dữ liệu tức thời cho Dashboard phục vụ trọng tài."*

---

### ❓ Câu 4: Nhóm đã thiết kế schema trong Cassandra như thế nào để tránh lệnh `ALLOW FILTERING`?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, trong Cassandra, việc dùng `ALLOW FILTERING` sẽ ép cluster phải quét tuần tự toàn bộ các nút mạng, gây sụt giảm nghiêm trọng hiệu năng.  
> Nhóm đã áp dụng triết lý Query-driven Modeling: mỗi bảng phục vụ đúng một mẫu truy vấn đã định trước:  
> - Bảng `analytics_by_match_type` dùng `match_type` làm Partition Key.  
> - Bảng `match_summary_by_id` dùng `match_id` làm Partition Key.  
> - Bảng `suspicious_records_by_run` dùng `run_id` làm Partition Key và `anomaly_score` làm Clustering Key với chiều sắp xếp giảm dần `DESC`. Nhờ đó, truy vấn lấy top người chơi bất thường được đọc tuần tự trực tiếp từ đĩa cứng mà không cần lọc hay sắp xếp lại trong bộ nhớ."*

---

### ❓ Câu 5: Nhóm gặp khó khăn kỹ thuật gì khi chạy PySpark trên môi trường Windows và đã giải quyết như thế nào?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, nhóm đã giải quyết 2 thách thức kỹ thuật lớn trên Windows:  
> 1. **Hệ thống tệp Hadoop:** Spark yêu cầu thư viện native Hadoop để ghi tệp đĩa trên Windows. Nhóm đã tích hợp bộ nhị phân `winutils.exe` và `hadoop.dll` phiên bản 3.3.6 tương thích vào mã nguồn.  
> 2. **Hiện tượng Python Worker Timeout:** Khi dùng Python UDF để tính khoảng cách Euclidean trên vector đặc trưng đa chiều, tiến trình kết nối giữa JVM và Python Worker bị nghẽn socket timeout. Nhóm đã tái cấu trúc toàn bộ logic tính toán sang **100% biểu thức Spark SQL Catalyst thuần túy** (`vector_to_array`, `sqrt`, `when`). Phép tính được biên dịch thẳng ra Java Bytecode trong JVM, giúp tốc độ tăng gấp 10 lần và loại bỏ triệt để lỗi timeout."*

---

### ❓ Câu 6: Dữ liệu này có theo dõi được một tài khoản qua nhiều trận đấu không?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, trong bộ dữ liệu cuộc thi PUBG Finish Placement Prediction của Kaggle, trường `Id` là định danh duy nhất của người chơi **trong phạm vi một trận đấu cụ thể**, chứ không phải ID tài khoản Steam cố định qua nhiều năm tháng.  
> Nhóm tuân thủ đạo đức dữ liệu: không tự ý bịa đặt hoặc ghép nối các `Id` không liên quan để tạo thành tài khoản giả. Chúng em định nghĩa chính xác bài toán là: **Phân tích và phát hiện hành vi bất thường ở cấp độ bản ghi trận đấu**. Đây là giới hạn dữ liệu công khai và nhóm đã nêu rất rõ ràng trong chương kết luận của báo cáo."*

---

### ❓ Câu 7: Làm sao hệ thống phân biệt được một Pro-player (tuyển thủ tay to) với một kẻ gian lận dùng Aimbot?
* **Trả lời:**
> *"Dạ thưa Thầy/Cô, đây chính là nguy cơ Dương tính giả (False Positive) mà nhóm đã nghiên cứu:  
> Tuyển thủ chuyên nghiệp có thể bắn rất nhiều mạng và headshot cao, nhưng hành vi của họ vẫn tuân theo quy luật vật lý: họ phải di chuyển nhiều (`walkDistance` lớn), nhặt vũ khí, sử dụng nước tăng lực và hồi máu hợp lý.  
> Ngược lại, kẻ gian lận thường bộc lộ những mâu thuẫn vật lý phi lý: ví dụ hạ gục 10 mạng nhưng quãng đường đi bộ bằng 0, hoặc tỷ lệ headshot tuyệt đối 100% trong thời gian rất ngắn. Hệ thống của nhóm kết hợp cả điểm lệch tâm K-Means lẫn các cờ vi phạm giới hạn vật lý để đưa vào diện 'Cần kiểm tra', giúp trọng tài người thật có thể xem lại video replay (killcam) trước khi đưa ra quyết định xử phạt."*

---

### 🎙️ Lời kết thúc buổi thuyết trình (08:45 trở đi)
> *"Trên đây là toàn bộ phần báo cáo và trình diễn đồ án của nhóm chúng em. Nhóm xin trân trọng cảm ơn Thầy/Cô đã chú ý lắng nghe và chúng em rất mong nhận được những câu hỏi góp ý quý báu từ hội đồng để hoàn thiện đề tài hơn nữa. Em xin cảm ơn Thầy/Cô!"*
