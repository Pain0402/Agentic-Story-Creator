# LỘ TRÌNH PHÁT TRIỂN DỰ ÁN - PHẦN 1 (Phiên bản v1.0 & v2.0)

## Giai Đoạn 1: Nghiên Cứu & Xây Dựng Proof of Concept (v1.0)
**Thời gian dự kiến:** 4 Tuần

### Tuần 1: Setup Môi Trường & Khảo Sát Kịch Bản
- **Công việc:**
  - Thiết lập môi trường Python, GPU (Local/Colab/RunPod) và cài đặt các thư viện cần thiết (LangChain, Diffusers, PyTorch).
  - Thu thập và chuẩn hóa tập dữ liệu mẫu: 20-30 kịch bản truyện ngắn thể loại Slice-of-life/Hành động.
  - Phân tích cấu trúc kịch bản theo định dạng tiêu chuẩn (Cảnh, Nhân vật, Lời thoại, Hành động).

### Tuần 2: Xây Dựng Tác Tử Phân Tích (Narrative Parsing Agent)
- **Công việc:**
  - Xây dựng prompt templates cho LLM đóng vai trò mổ xẻ kịch bản.
  - Lập trình hệ thống trích xuất JSON đầu ra chứa: `panel_count` (số lượng khung), `characters`, `setting`, `action_description`, `dialogue`.
  - Kiểm định độ chính xác của Agent qua 10 kịch bản mẫu.

### Tuần 3: Xây Dựng Tác Tử Đồ Họa Cơ Bản (Consistent Generation Agent - Mức 1)
- **Công việc:**
  - Tích hợp API tạo ảnh (Stable Diffusion WebUI API hoặc ComfyUI API).
  - Viết pipeline chuyển đổi mô tả hành động (từ JSON tuần trước) thành Prompt tạo ảnh truyện tranh.
  - Bước đầu chạy thử text-to-image để đánh giá thẩm mỹ và phong cách (Style: Anime/Webtoon).

### Tuần 4: Chắp Ghép & Đánh Giá Điểm Nghẽn v1.0
- **Công việc:**
  - Nối luồng (Pipeline): Kịch bản văn bản -> JSON -> Prompts -> 5 ảnh rời rạc.
  - Kiểm tra độ đứt gãy mạch truyện (sai nhân vật, sai góc nhìn).
  - Lập tài liệu báo cáo v1.0, tổng hợp các điểm mù để giải quyết ở v2.0.

---

## Giai Đoạn 2: Quản Lý Bố Cục & Tính Nhất Quán (v2.0)
**Thời gian dự kiến:** 5 Tuần

### Tuần 5-6: Xây Dựng Tác Tử Bố Cục (Layout Generation Agent)
- **Công việc:**
  - Nghiên cứu Ngữ pháp tự sự trực quan (Visual Narrative Grammar).
  - Tạo thuật toán phân chia hình chữ nhật cho Webtoon (chiều cuộn dọc, tỷ lệ 1:1, 16:9, khung vát chéo).
  - Xây dựng bộ quy tắc: Độ dài script ngắn -> Panel nhỏ; Cực điểm cảm xúc -> Panel lớn chiếm trọn trang.
  - Ánh xạ JSON nội dung kịch bản vào các hộp bố cục (Bounding boxes).

### Tuần 7-8: Áp Dụng Reference Bank & Kiểm Soát Nhân Vật
- **Công việc:**
  - Cài đặt và cấu hình IP-Adapter hoặc huấn luyện nhanh LoRA cho 2-3 nhân vật mẫu.
  - Tích hợp ControlNet (OpenPose/Depth) để Tác tử đồ họa giữ đúng góc camera hoặc dáng người được quy định bởi Tác tử bố cục.
  - Liên kết Tác tử Bố cục và Tác tử Đồ họa: Sinh hình ảnh với độ phân giải/Tỷ lệ chính xác với khung được cấp.

### Tuần 9: Ghép Trang Webtoon v2.0 & Fix Lỗi
- **Công việc:**
  - Sử dụng module Python (như Pillow/OpenCV) để dán các bức ảnh sinh ra vào tấm canvas dọc khổng lồ.
  - Đo lường đánh giá SSIM/FID để kiểm tra độ "bền" hình dáng nhân vật xuyên suốt khung 1 tới khung 10.
  - Học lại phản hồi (Retrospective) chuẩn bị qua v3.0.
