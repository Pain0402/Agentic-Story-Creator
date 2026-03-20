# TÀI LIỆU BONUS 5: ĐẶC TẢ GIAO DIỆN NGƯỜI DÙNG VÀ TRẢI NGHIỆM (UI/UX DOMAIN DESIGN)

Đồ án luận văn sẽ có tính "thuyết phục thực tiễn" cao nếu bạn đóng gói kiến trúc phức tạp thành một sản phẩm dễ sử dụng (SaaS Mockup / Web Application). Dưới đây là sườn kỹ thuật thiết kế Giao diện (Frontend) để giao tiếp với các Tác tử của bạn.

## 1. Triết Lý Thiết Kế (Design Philosophy)
Người dùng Web là tác giả, không phải nhà khoa học. Họ không cần biết ControlNet là gì.
- Toàn bộ thiết lập AI (Denoise, CFG Scale) bị **ẩn** (Hidden). Có nút Advanced Settings nếu cần.
- Sử dụng màn hình chia đôi (Split Screen): Một bên là Kịch bản chữ, một bên là Canvas xem trước truyện tranh trực quan. Thay đổi chữ bên trái -> Ảnh bên phải cập nhật theo yêu cầu.

## 2. Giao Diện Bàn Điều Khiển (Dashboard UI - Flow)

### Màn Hình 1: Project Setup (Khởi Tạo Dữ Liệu)
- Ô input lớn: "Dán kịch bản / Dàn ý tiểu thuyết / Truyện ngắn của bạn vào đây".
- Tải lên ảnh thiết kế hình dáng các nhân vật chính (Reference Image Upload). Gắn nhãn tên, VD: Mập (Fat), Lính (Soldier).
- Chỉnh Phong cách bằng 1 click: Bảng màu Anime (Màu sắc tươi), Phong cách Goth/Cyberpunk (Tối tăm), Manga trắng đen.

### Màn Hình 2: Editor (Sửa Bố Cục - Layout Approval) 
*Nhiệm vụ của Tác Tử: Báo cáo kết quả "Phân mảnh kịch bản" cho người viết duyệt.*
- Nửa trái là danh sách kịch bản đã được tô sáng (Highlight) bởi Phân tích ngữ cảnh (Narrative Agent). Thấy các "Cảnh" nối tiếp nhau (Ví dụ: Cảnh 1 - Quán trà; Cảnh 2 - Nhảy lầu).
- Nửa phải: Bố cục Canvas trống vạch ra sẵn các Hình Rỗng (Boxes outline) định hình bố cục trang webtoon, chưa phải vẽ ngay (Tiết kiệm tài nguyên GPU).
- Nếu User thấy ô to này không vừa ý, ấn nút Kéo/Thả đổi kích thước khung.

### Màn Hình 3: Generation & Review Canvas (Sinh Ảnh Cực Đại)
1. User nhấn "Generate All Panels". Loading spinner hiển thị Tiến độ kết hợp giữa 4 Tác tử tính bằng tỷ lệ %.
2. Nửa phải trả về kết quả ảnh mượt mà có chữ thoại đầy đủ, đọc theo định dạng dọc.
3. Tooltip: Rê chuột vào một Box (Ví dụ Box 3), hộp công cụ nhỏ (Toolbar) nổi lên: 
   - `[Tuỳ Biến Chữ]`: User có thể kéo bong bóng thoại từ mặt nhân vật xuống cạnh chân nhân vật.
   - `[Tạo Lại Hình Nghệ Thuật Này]`: Agent 3 sẽ chạy lại hạt giống mới (seed) cho riêng Box 3 (không làm liên đới mất công Box 2, Box 4).

### Màn Hình 4: Export (Kết Xuất Môi Trường)
- Tải về Định dạng ZIP bao gồm N ảnh dài liên tiếp (Resolution 1080 x 1920).
- Hoặc xuất ra Project Source File chứa toàn bộ JSON cấu trúc lưới và Layout metadata.

## 3. Kiến Trúc API Trả Về Giữa UI & AI Backend (Interface Specification)
Frontend gọi Backend bằng POST request. Response JSON nên có dạng:
```json
{
  "status": "success",
  "project_id": "WEBTOON_9999",
  "webtoon_canvas_url": "https://s3.aws.com/assets/canvas_01.png",
  "panels_metadata": [
    {"id": "p_1", "coordinates": {"x": 0, "y": 0, "w": 800, "h": 600}, "img_layer": "link_ảnh_1.png", "text_layer": ["Xin chàooo!"]}
  ]
}
```
Thiết kế dữ liệu dạng Layer (Lớp ảnh + Lớp chữ) giúp người dùng trên giao diện có thể dễ dàng tắt/bật lớp chữ để chỉnh nền ảnh. Điều này làm ứng dụng cực kỳ linh hoạt và "Pro".
