# KẾ HOẠCH TRIỂN KHAI DỰ ÁN: ANIMEAI WEBTOON (GIAI ĐOẠN 3 - v3.0)

## 📌 Tổng Quan
- **Mục tiêu:** Xây dựng Tác tử Thông minh có khả năng nhận diện hình ảnh (Thị giác máy tính / VLM) để tối ưu hóa vị trí Bong bóng thoại (tránh đè nhân vật) và tự động hóa toàn bộ quy trình từ text đến Webtoon hoàn chỉnh (End-to-End Pipeline). Thêm cơ chế Tự phản biện (Critic Agent) để sửa lỗi ảnh.
- **Loại Dự án:** COMPUTER VISION, VLM AUTONOMOUS AGENT & PIPELINE INTEGRATION.
- **Thời gian dự kiến:** 4 Tuần.

## 🎯 Tiêu Chí Thành Công v3.0
1. Bong bóng thoại tự động lách khỏi khuôn mặt nhân vật nhờ thuật toán nhận diện khuôn mặt (OpenCV/Mediapipe).
2. Viết thành công 1 kịch bản chạy Tuyến tính từ Nhập Text -> Xuất PNG Webtoon Hoàn Chỉnh (Không cần can thiệp tay).
3. Bổ sung Critic Agent giám sát chất lượng ảnh sinh ra để tự động gọi lại quá trình tạo ảnh nếu phát hiện lỗi nặng.

## 📋 Phân Rã Nhiệm Vụ (Task Breakdown)

### Tuần 10: Xây Dựng Tác Tử Sắp Chữ "Ngắm Mục Tiêu" (Smart Typography Agent)
- ✅ **Task 18:** Tích hợp Thị giác máy tính (Computer Vision) để nhận diện khuôn mặt.
  - **Agent:** `backend-specialist`
  - **Input:** Cài đặt OpenCV (`cv2`) và cấu hình mô hình nhận diện khuôn mặt (Haar Cascades hoặc YOLO/Mediapipe).
  - **Output:** Hàm nhận vào một ảnh Panel và trả về tọa độ `(x,y,w,h)` của các khuôn mặt trong ảnh để đánh dấu Vùng cấm (Red Zone).
  - **Verify:** Script chạy in ra danh sách tọa độ mặt trên màn hình terminal.
- ✅ **Task 19:** Nâng cấp thuật toán Gắn Bóng Thoại (Smart Bubble Placement).
  - **Agent:** `backend-specialist`
  - **Input:** Tọa độ khuôn mặt từ Task 18. Code `speech_bubble.py` hiện tại.
  - **Output:** Thuật toán tự tìm "Vùng an toàn" (Safe zone) - khoảng trống không chứa mặt người - để đặt bong bóng thoại.
  - **Verify:** Bong bóng thoại trên bức ảnh `final_webtoon_story.png` tự né sang góc khác khi nhân vật chiếm góc dưới.

### Tuần 11: Đóng Gói Dây Chuyền Tự Động (Pipeline Integration)
- ✅ **Task 20:** Tạo Hàm Cốt Lõi (Core Pipeline Engine).
  - **Agent:** `orchestrator`
  - **Input:** Liên kết Narrative -> Layout -> ComfyUI -> Stitching -> Smart Bubble.
  - **Output:** Một file `src/backend/engine.py` gọi chuỗi mắc xích tự động.
  - **Verify:** Chỉ cần nhập 1 biến `text` và máy tự chạy hết 100% công đoạn tạo truyện.

### Tuần 12: Xây Dựng Cơ Chế "Tự Kiểm Duyệt" (Critic Feedback Loop)
- ✅ **Task 21:** Khởi tạo Tác Tử Hình Ảnh (Critic Agent).
  - **Agent:** `project-planner` / `backend-specialist`
  - **Input:** Sử dụng Gemini Vision API (hoặc cài đặt đánh giá aesthetic local).
  - **Output:** Một endpoint nhận ảnh vừa sinh ra, đánh giá xem có bị "biến dạng" không. Nếu có, gửi tín hiệu "Regenerate" về ComfyUI.
  - **Verify:** Logs hệ thống ghi nhận "Phát hiện lỗi bàn tay 6 ngón -> Đang sinh lại ảnh".

*(Tuần 13 sẽ dành cho việc Benchmark đo thông số API để viết Luận văn sau khi API hoàn thiện)*
