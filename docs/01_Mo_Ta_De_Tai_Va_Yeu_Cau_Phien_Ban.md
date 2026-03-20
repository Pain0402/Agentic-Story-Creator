# TÀI LIỆU MÔ TẢ ĐỀ TÀI VÀ YÊU CẦU PHIÊN BẢN (RELEASES)

## 1. Tên Đề Tài
**Hệ thống tác tử đa trí tuệ phân cấp cho việc chuyển đổi Kịch bản tự sự sang Storyboard Manga định dạng đọc dọc (Hierarchical Multi-Agent System for Automated Narrative-to-Webtoon Storyboard Conversion)**

## 2. Mô Tả Chi Tiết Đề Tài
Đề tài nghiên cứu và phát triển một hệ thống tự động hóa hoàn toàn quy trình chuyển đổi từ một kịch bản truyện thô (văn bản) thành một bản phân cảnh Webtoon (Storyboard cuộn dọc) sẵn sàng xuất bản. 
Điểm đột phá của đề tài là việc ứng dụng **Kiến trúc Tác tử Đa trí tuệ phân cấp (Hierarchical Multi-Agent System)**, thay vì sử dụng một mô hình duy nhất. Các tác tử (Agents) sẽ đóng vai trò như những chuyên gia thực thụ trong phòng biên tập:
- **Tác tử Phân tích (Narrative Parsing Agent):** Mổ xẻ kịch bản, nhận diện sự kiện, cảm xúc và nhân vật.
- **Tác tử Bố cục (Layout Generation Agent):** Áp dụng Ngữ pháp tự sự trực quan để chia khung (paneling) sao cho hợp lý nhất theo định dạng cuộn dọc.
- **Tác tử Đồ họa (Consistent Generation Agent):** Vẽ và duy trì tính nhất quán hình ảnh dựa trên bộ nhớ nhân vật (Reference Bank) tích hợp ControlNet/IP-Adapter.
- **Tác tử Sắp chữ (Typography Agent):** Đặt bong bóng thoại tự động sao cho không che khuất mặt và dắt mắt người đọc trôi chảy.

Mục tiêu cuối cùng là đóng gói toàn bộ quy trình này thành một ứng dụng web/SaaS, nơi người dùng chỉ cần nhập kịch bản, chọn phong cách (Style) và nhận về thành phẩm Storyboard chất lượng cao.

## 3. Mục Tiêu Nghiên Cứu
- **Khoa học:** Đề xuất một cấu trúc liên kết chuẩn xác giữa NLP (hiểu kịch bản) và Computer Vision (phân bổ không gian & sinh ảnh) để giải quyết "Cascading Errors" (lỗi dây chuyền) trong các luồng Agentic.
- **Thực tiễn:** Xây dựng phần mềm giúp giảm 80% thời gian lên Storyboard của họa sĩ Webtoon, đưa quá trình xuất bản đến gần hơn với các tác giả không rành vẽ.

## 4. Các Yêu Cầu Cần Đạt Được Theo Từng Phiên Bản (Version Requirements)

### Phiên Bản 1 (v1.0): Proof of Concept (Cơ bản)
*Mục tiêu:* Chứng minh tính khả thi của việc liên kết các Agents.
- **Yêu cầu:** 
  - Khởi tạo được 2 Tác tử cơ bản: Narrative Parsing Agent (sử dụng GPT API/Claude) để tách câu kịch bản & Consistent Generation Agent (Stable Diffusion/Flux) tạo ảnh từ text rời rạc.
  - Sinh ra được 3-5 ảnh rời rạc tương ứng với kịch bản nhưng **chưa** cần có bố cục khung dọc phức tạp.
  - Hình ảnh sinh ra ở mức độ chấp nhận được, có nhận diện nhân vật cơ bản (chưa cần nhất quán 100%).

### Phiên Bản 2 (v2.0): Layout & Character Consistency (Nhất quán & Cấu trúc)
*Mục tiêu:* Áp dụng thuật toán chia khung và chốt thiết kế nhân vật.
- **Yêu cầu:** 
  - Tích hợp Layout Generation Agent: Sinh ra các hộp khung (boxes) theo chiều cuộn dọc dựa trên tỷ lệ trang.
  - Ứng dụng ControlNet/IP-Adapter/LoRA để duy trì thiết kế nhân vật xuyên suốt qua các khung truyện khác nhau.
  - Cắt ghép các ảnh tĩnh do Tác tử đồ họa sinh ra vào đúng các khung bố cục đã định. Kết quả đầu ra là 1 trang Webtoon hoàn chỉnh (nhưng chưa có chữ).

### Phiên Bản 3 (v3.0): Full Pipeline & Typography (Sắp chữ & Tối ưu luồng)
*Mục tiêu:* Hoàn thành toàn bộ luồng tạo truyện có chữ.
- **Yêu cầu:**
  - Phát triển Typography Agent: Thuật toán xác định vị trí vùng trống (negative space) trong ảnh để chèn bong bóng thoại.
  - Tích hợp tự động chèn chữ vào bong bóng thoại với phông chữ truyện tranh chuẩn.
  - Xây dựng cơ chế *Feedback Loop* cơ bản: Nếu Typography không thể đặt bóng thoại vì hết chỗ, nó yêu cầu thuật toán ảnh tạo lại khung với vùng đệm rộng hơn.
  - Kết xuất (Export) file cuộn dọc định dạng PNG/JPG tiêu chuẩn (800x1280px / frame).

### Phiên Bản 4 (v4.0): Web Application & Optimization (Sản phẩm cuối)
*Mục tiêu:* Frontend thân thiện, tối ưu hóa tốc độ.
- **Yêu cầu:**
  - Triển khai ứng dụng Web (React/Next.js) cho phép người dùng nhập kịch bản qua giao diện.
  - Có tính năng xem trước (Preview) và chỉnh sửa lại từng khung (Human-in-the-loop). Người dùng có quyền can thiệp thay ảnh của một khung bất kỳ.
  - Tối ưu hóa thời gian xử lý tổng thể dưới 5 phút cho một Chapter ngắn.
  - Sẵn sàng tài liệu API, System Architecture cho Lễ bảo vệ luận văn.
