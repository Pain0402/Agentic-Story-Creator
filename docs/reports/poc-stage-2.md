# KẾ HOẠCH TRIỂN KHAI DỰ ÁN: ANIMEAI WEBTOON (GIAI ĐOẠN 2 - v2.0)

## 📌 Tổng Quan
- **Mục tiêu:** Xây dựng cỗ máy tính toán Bố cục (Layout Generation Agent), giải quyết yếu điểm ảnh rời rạc của v1.0. Biến các khung ảnh thành một dải Webtoon cuộn dọc hoàn chỉnh, chừa không gian trống (Negative Space) cho bóng thoại.
- **Loại Dự án:** MICROSERVICES BACKEND & ALGORITHMIC LAYOUT.
- **Thời gian dự kiến:** 5 Tuần.

## 🎯 Tiêu Chí Thành Công v2.0
1. Từ file JSON ở Giai đoạn 1, hệ thống sinh ra được file JSON Tọa độ Bố cục (Có x, y, width, height cụ thể cho từng ô truyện).
2. Ứng dụng thuật toán **Ngữ pháp Thị giác (Visual Narrative Grammar)**: Hành động mạnh sinh khung lớn nhô ra ngoài viền, hội thoại lê thê sinh khung kín nhỏ.
3. Vẽ thành công bản nháp Skeleton (Xương sườn) bằng hộp đen trắng trên Canvas trải dài 10,000px trước khi chuyển xuống thư mục AI Engine sinh màu sắc.

## 📋 Phân Rã Nhiệm Vụ (Task Breakdown)

### Tuần 5: Xây Dựng Lõi Thuật Toán Bố Cục (Layout Generation)
- ✅ **Task 10:** Xây dựng Schema Bố cục (`layout_schema.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Định nghĩa Pydantic cho Layout gồm thông số x, y, tọa độ tuyệt đối, tỷ lệ khung (aspect ratio).
  - **Output:** File `src/backend/models/layout_schema.py`.
  - **Verify:** Lớp dữ liệu biên dịch không lỗi trùng lặp namespace.
- ✅ **Task 11:** Khởi tạo Tác Tử Bố Cục (`layout_agent.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Khai thác dữ liệu `action_intensity` (mức độ từ 1-5). Thuật toán tự chia khoảng cách viền (gutter).
  - **Output:** File `src/backend/agents/layout_agent.py` tự động tính tọa độ xuống dọc.
  - **Verify:** Script chạy in ra Array tọa độ bounding box 2D.
- ✅ **Task 12:** Lập trình Bộ Khung Xương Hình Ảnh (`draw_layout.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Dữ liệu tọa độ từ Task 11. Cài đặt thư viện `Pillow`.
  - **Output:** Hàm nhận JSON và lưu ra 1 bức ảnh `.png` dài chứa các ô vuông đen có đánh số 1, 2, 3...
  - **Verify:** Xuất ra được ảnh `dummy_webtoon.png` hoàn hảo không chạm mép.

### Tuần 6: Khớp Nối API (Narrative + Layout) & Chỉnh Sửa Workflow AI
- ✅ **Task 13:** Hợp nhất luồng Dữ liệu vào FastAPI (`main.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Kết nối Code LLM (Task 5) và Code Bố cục (Task 11).
  - **Output:** Endpoint `/api/v2/generate-layout` nhận Text và trả về Toàn bộ Script + Bounding Box.
  - **Verify:** Endpoint hoạt động ổn định trên Postman/cURL.
- ✅ **Task 14:** Cập nhật Workflow ComfyUI tương thích Bố Cục (`comfyui_client.py`).
  - **Agent:** `backend-specialist`
  - **Input:** JSON Workflow cũ từ v1.0. Tái cấu trúc JSON gửi lên Ngrok sao cho độ phân giải của ảnh sinh ra (`width`, `height`) phải mượt mà khớp đúng tỷ lệ (Aspect Ratio) mà Layout Agent đưa xuống.
  - **Output:** Mã API tự động tính toán Size để truyền cho ComfyUI.

### Tuần 7: Image Stitching (Lắp ráp Tranh Cuộn) & Character Consistency
- ✅ **Task 15:** Tráng ghép Ảnh AI vào Tấm Bạt Xương Sườn (`stitch_webtoon.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Ảnh vẽ từ Colab rớt về máy. Canvas với hình vuông từ Task 12.
  - **Output:** Script Python (Pillow) tự động Scale ảnh vừa vặn và DÁN (Paste) thẳng vào đúng ô tọa độ Txt2Img tương ứng, tạo thành 1 file PNG Webtoon thực thụ!
  - **Verify:** Một bức ảnh Cuộn Dọc chứa cả màu sắc, đúng vị trí.
### Tuần 8: Gắn Bóng Thoại (Speech Bubble) & Khống Chế Khuôn Mặt
- ✅ **Task 16:** Thuật toán gắn Bóng Thoại lên Canvas (`speech_bubble.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Script hội thoại từ Narrative JSON, tọa độ Panel từ Layout.
  - **Output:** Dùng Pillow vẽ khung Rounded Rectangle và Text (Gắn ở dưới đáy Panel hoặc góc trên). Đảm bảo Text tự động xuống dòng (Word Wrap).
  - **Verify:** Chạy script và nhìn thấy chữ nổi lềnh bềnh trên bề mặt của trang Webtoon mà không đè mất quá nhiều vào mặt Cảnh chính.
- ✅ **Task 17:** Bổ sung Workflow Giữ vững Khuôn mặt (IP-Adapter).
  - **Agent:** `backend-specialist`
  - **Input:** JSON Workflow mới của ComfyUI có chứa cụm node `IP-Adapter` (Dùng 1 tấm ảnh chân dung làm hạt giống tham chiếu).
  - **Output:** Tích hợp JSON này thay cho mã Txt2Img thuần túy ở Task 14, ép nhân vật sinh ra qua các Khung phải giống nhau 90%.
  - **Verify:** Xem 3 khung ảnh và xác nhận quần áo, màu tóc không tự thay đổi ngẫu nhiên.
