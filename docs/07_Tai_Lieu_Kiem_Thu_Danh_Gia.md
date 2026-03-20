# KẾ HOẠCH ĐÁNH GIÁ VÀ KIỂM THỬ THỰC NGHIỆM

Để Luận văn đạt điểm tối đa, hệ thống phải được chứng minh bằng các phép đo lường (Metrics) có cơ sở khoa học thay vì chỉ là "chạy đồ án thấy đẹp". Tài liệu này mô tả kịch bản kiểm thử cho từng chương.

## 1. Đánh Giá Khách Quan Bằng Thuật Toán (Quantitative Metrics)

### 1.1 Bài Kiểm Tra Độ Nhất Quán Nhân Vật (Character Consistency Test)
Mục tiêu: Đảm bảo Tác tử Đồ họa (Consistent Generation Agent) duy trì được nhận diện nhân vật qua 10 khung hình khác nhau.
- **Phương pháp:** 
  1. Cung cấp một hình ảnh tham chiếu nhân vật góc chính diện (Reference Image) chứa một nhân vật có đặc điểm phức tạp (Ví dụ: Đeo kính, tóc hai màu, trang phục nhiều họa tiết).
  2. Tạo tự động 10 khung truyện có nhân vật đó ở các góc nhìn khác nhau (Nghiêng, nhìn từ trên xuống, từ dưới lên).
- **Thước đo:** Tính toán chỉ số **SSIM** (Structural Similarity Index) hoặc **LPIPS** giữa khuôn mặt ở ảnh sinh ra và ảnh tham chiếu rễ (Reference Bank). Chỉ số LPIPS càng thấp (với Embeddings của khuôn mặt), độ nhất quán càng cao, chứng tỏ mô hình không sinh lỗi.

### 1.2 Bài Kiểm Tra Độ Che Khuất Văn Bản (Occlusion/Typography Test)
Mục tiêu: Đảm bảo Typography Agent không gắp bong bóng thoại (Speech bubbles) dán đè lên "Vùng quan trọng" (khuôn mặt, hành động).
- **Phương pháp:** Sinh 50 bong bóng thoại tự động trên 50 khung cảnh. Sử dụng công cụ Object Detection (như YOLOv8) quét lại các ảnh vừa sinh để tìm "Khuôn mặt". 
- **Thước đo:** Tính tỷ lệ Intersection over Union (IoU) giữa hộp bong bóng thoại và hộp khuôn mặt. Nếu IoU > 0.05, tức là chữ đã đè lên mặt (LỖI). Đặt mục tiêu tỷ lệ Pass Rate đạt > 95%.

### 1.3 Hiệu Năng & Độ Trễ (Performance & Latency Test)
- **Phương pháp:** Đo thời gian end-to-end từ khi ấn nút "Generate" tới khi có kết quả hoàn chỉnh (1 Trang Webtoon gồm 5 khung).
- **Thước đo:** 
  - Token/s cho khâu phân tích kịch bản.
  - Số giây để hoàn thành Inference ảnh với bước lấy mẫu (Sampling steps) là 20. Độ trễ mục tiêu phải dưới 3 phút/trang trên card RTX 409x hoặc A10G Cloud.

## 2. Đánh Giá Chủ Quan Từ Chuyên Gia / Người Dùng (Qualitative / UAT)
Sử dụng phương pháp **Human-In-The-Loop Survey** hoặc **Turing Test for Comics**.
- **Kịch bản:** Mời 10 người tham gia (5 sinh viên bình thường, 5 người từng đọc/vẽ Webtoon).
- **Mẫu khảo sát:** Cho xem 3 trang Manga được vẽ bằng quy trình AI mới vs 3 trang vẽ bằng "AI Cũ" (Midjourney/DALL-E sinh rời rạc).
- **Tiêu chí chấm điểm (Thang Likert 1-5):**
  1. *Tính mạch lạc của cốt truyện (Narrative Flow):* Người đọc có hiểu diễn biến từ khung 1 đến khung cuối không?
  2. *Chất lượng hình ảnh (Aesthetic Score):* Phong cách nghệ thuật có đồng nhất không? (Việc áo đang màu xám tự nhiên khung sau thành áo màu xanh trừ điểm nặng).
  3. *Mức độ chuyên nghiệp của Bố cục (Layout Dynamism):* Các khung Panel được chia có sự thay đổi lớn nhỏ hợp lý với nhịp độ hành động (đánh nhau thì khung vát chéo/to, nói chuyện bình thường thì khung ngang) hay không?

## 3. Nhật Ký Lỗi & Gỡ Rối (Bug Triage & Root Cause Analysis)
Lập trình viên cần duy trì một tài liệu log ghi nhận:
- Khi nào Agent bị Hallucinate (LLM chế thêm lời thoại không có trong kịch bản).
- Khi nào Diffusion model vẽ dư ngón tay (Cách khắc phục: Bật Tác tử Kiểm duyệt/Critic Agent tự động detect hoặc Thêm keyword "6 fingers" vào Negative Prompt).
- Bong bóng thoại bị tràn viền (Cách xử lý: Limit ký tự mỗi bong bóng, tự động bẻ dòng dựa trên fontsize).
