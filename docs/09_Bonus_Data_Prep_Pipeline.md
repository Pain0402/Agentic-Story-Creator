# TÀI LIỆU BONUS 2: CƠ CHẾ LOGIC CỦA TÁC TỬ BỐ CỤC VÀ SẮP CHỮ 
*(Layout & Typography Pipeline)*

Bản sắc của truyện Webtoon là khả năng vuốt/cuộn (Scrolling) với các khung hình vát chéo đan xen không gian trống. Tài liệu này cung cấp tư duy logic cho Lập trình viên để triển khai Backend ở các Module khó nhất.

## 1. Logic Sinh Bố Cục Đọc Dọc (Layout Agent Algorithm)

Thay vì đặt các ô đều nhau (Lưới Grid) như truyện tranh Mỹ, hãy xây dựng một "Bộ quy tắc Ràng buộc Kích thước" (Size Constraint Rules System):

**Tham số đầu vào:** JSON chứa `panels` từ Lớp 1 (Narrative), bao gồm biến số cực kì quan trọng: `action_intensity` (1 - 5).

**Thuật toán:**
Giả sử Canvas chiều rộng là dọc cố định: `Width = 800px`, `Height` mở rộng vô hạn xuống dưới.
- Khởi tạo `y_offset = 0`.
- Vòng lặp duyệt qua từng `panel` trong danh sách:
  1. Nếu `action_intensity == 1` (Khung hội thoại ngắn): Tạo ô vuông nhỏ tỷ lệ 1:1, căn trái hoặc căn phải cho 2 khung xen kẽ.
  2. Nếu `action_intensity == 3` (Khung giới thiệu quang cảnh): Tạo ô rộng chữ nhật 16:9 lấp đầy chiều rộng Canvas.
  3. Nếu `action_intensity == 5` (Cao trào, nhân vật thức tỉnh, đánh nhau): Chiều cao của khung phải gấp đôi bình thường, không có lề màn hình (Bleed frame), loại bỏ toàn bộ khoảng trắng xung quanh.
- Cộng `y_offset` xuống phía dưới kèm một khoảng đệm 100px (margin) cho khoảng trắng đọc (Gutter).

Đầu ra của Node code này phải trả về là một danh sách các tọa độ Box: `[x, y, width, height]` của từng ảnh. Đẩy tọa độ này cho công cụ ghép ảnh (Pillow).

## 2. Logic Tránh Mục Tiêu Nhạy Cảm (Typography & Occlusion Avoidance)
Vấn đề lớn của truyện tự động là chữ đè lên mắt, lên mũi nhân vật.

**Các bước cho Auto-Bubble Placement:**
1. **Detect (Phân tích Mask):** Đưa tấm ảnh sinh ra ở bước 3 qua một model nhận diện như YOLOv8 (đã train để quét khuôn mặt Anime) hoặc thư viện xử lý điểm ảnh. Xác định các "Vùng Cấm" (Forbidden Zones).
2. **Search (Tìm vùng an toàn):** Tính toán độ tương phản vùng ảnh tĩnh. Một góc trên bên phải bầu trời trống thường có độ biến thiên pixel (Gradient) thấp (rải màu rất phẳng). Chấm điểm vùng này là "Vùng an toàn cao điểm".
3. **Draw (Vẽ Vector):** Đoạn chữ thoại "Who are you?" có độ rộng 300px, 1 dòng 100px. Thuật toán Box Fitting sẽ quét "Vùng an toàn" có chứa lọt hình hộp 300x100 hay không.
4. **Render:** Vẽ Ellipse màu lõi trắng (Fill) viền đen (Stroke) dán vào tọa độ đó. Text được Render đè lên ở giữa có căn lề (Center alignment).

*Gợi ý công nghệ:* Các module Python như `OpenCV` (cv2), cấu trúc thư viện `Pillow` (ImageDraw) có sẵn đầy đủ đồ họa 2D vector để lấp và vẽ bong bóng thoại này mà không cần thư viện quá hầm hố.
