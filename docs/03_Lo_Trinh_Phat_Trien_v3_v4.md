# LỘ TRÌNH PHÁT TRIỂN DỰ ÁN - PHẦN 2 (Phiên bản v3.0 & v4.0)

## Giai Đoạn 3: Hoàn Thiện Tác Tử Sắp Chữ & Cơ Chế Phản Hồi (v3.0)
**Thời gian dự kiến:** 4 Tuần

### Tuần 10: Xây Dựng Tác Tử Sắp Chữ (Typography Agent)
- **Công việc:**
  - Tính toán vùng "An toàn" (Negative space): Sử dụng mô hình phân vùng hình ảnh (ví dụ: YOLO hoặc Segment Anything) để xác định vị trí bầu trời, góc trống không có mặt nhân vật.
  - Tạo thuật toán vẽ bong bóng thoại (Speech bubbles) hình Oval/Vuông bo góc theo độ dài text.

### Tuần 11: Render Chữ & Lắp Ráp Toàn Bộ Dây Chuyền
- **Công việc:**
  - Gắn font chữ phù hợp (Tác giả, font Manga/Anime convention).
  - Nối kịch bản Text (từ v1.0) -> Bố cục (v2.0) -> Ảnh (v2.0) -> Typography (v3.0).
  - Đóng gói toàn bộ mã nguồn Backend thành các dịch vụ độc lập (Micro-services hoặc một pipeline chạy tuyến tính).

### Tuần 12: Xây Dựng Cơ Chế "Tự Kiểm Duyệt" (Reflection/Feedback Loop)
- **Công việc:**
  - Thiết lập Tác tử "Tổng biên tập" (Critic Agent / Reviewer).
  - Nhiệm vụ: Xóa hoặc cảnh báo sinh lại nếu Tác tử Đồ họa sinh lỗi (ví dụ dư ngón tay) hoặc bong bóng thoại lẹm vào mắt nhân vật.
  - Chạy thử nghiệm với dữ liệu quy mô vừa (50 trang) và đánh giá độ chính xác thuật toán tự sửa lỗi.

### Tuần 13: Đóng Băng Tính Năng Core & Benchmark
- **Công việc:**
  - Tinh chỉnh các tham số (Hyperparameter tuning) như nhiệt độ của LLM (Temperature), cfg_scale của Diffusion model.
  - Lập tài liệu đo đạc chi phí API, tài nguyên GPU, thời gian tạo 1 trang.

---

## Giai Đoạn 4: Trải Nghiệm Người Dùng & Triển Khai (v4.0)
**Thời gian dự kiến:** 4 Tuần

### Tuần 14: Xây Dựng Giao Diện Người Dùng (Frontend)
- **Công việc:**
  - Lên thiết kế Figma cho Web App "Manga/Webtoon AI Copilot".
  - Code Frontend bằng ReactJS/Next.js. Có các tab: Soạn kịch bản, Thiết lập phong cách, Workspace (Canvas xem trước cấu trúc).
  - Thiết kế tính năng "Human-in-the-Loop": Cho phép người dùng click vào một khung bị lỗi và ấn "Regenerate".

### Tuần 15: Tích Hợp Hệ Thống (Frontend - Backend)
- **Công việc:**
  - Bọc Backend Pipeline thành các RESTful/GraphQL APIs (Sử dụng FastAPI).
  - Gắn Frontend vào Backend, thử nghiệm User Flow: Đăng nhập -> Tạo Project -> Nhập Kịch Bản -> Bấm Generate -> Tải về Webtoon JPG.

### Tuần 16: Kiểm Thử Chấp Nhận Hệ Thống (UAT)
- **Công việc:**
  - Mời 5-10 người dùng thật (Sinh viên, Content Creator) trải nghiệm dùng thử phần mềm sinh webtoon.
  - Thu thập Feedback Form về mức độ hài lòng, dễ dùng, chất lượng nội dung sinh ra.
  - Bug fixing chặn cuối (Final fixes).

### Tuần 17: Triển Khai Thực Tế & Viết Báo Cáo Luận Văn
- **Công việc:**
  - Chuyển source code Backend lên server có GPU (Ví dụ: RunPod, AWS EC2 g4dn) và deploy Frontend.
  - Tổng hợp số liệu đo đạc (Độ trễ, Hiệu suất, Tỉ lệ tạo lỗi).
  - Đổ số liệu vào file Latex/Word báo cáo luận văn (soạn thảo theo sườn quy định của Khoa).
