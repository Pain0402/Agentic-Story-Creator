# BÁO CÁO KIỂM THỬ END-TO-END (POC GIAI ĐOẠN 2 - v2.0)

## 📌 Thành Quả Đạt Được (What Worked)
1. **Kiến Trúc Bố Cục Tự Động (Algorithmic Layout Agent):** 
   - Đạt được chuẩn "Ngữ pháp thị giác" truyện tranh (Visual Narrative Grammar). 
   - Khắc phục triệt để luồng ảnh rời rạc của bản v1.0 bằng thuật toán tự chia tọa độ (Gutter spacing, Margin, Negative Space). 
   - Đặc biệt, hệ thống xử lý xuất sắc cụm khung dọc (9:16) cho cảnh cao trào và gộp cụm khung theo cặp (Side-by-side clustering) cho các cảnh hội thoại nhẹ tĩnh lặng.
2. **Kỹ Thuật Cắt Dán & Tráng Chữ Động (Image Stitching & Speech Bubbles):** 
   - Công cụ `stitch_webtoon.py` và `speech_bubble.py` hoạt động đồng nhất. Nó ép kích cỡ (Resize/Crop Lanczos) bức ảnh AI sao cho vừa vặn tuyệt đối vào Khung xương (Skeleton).
   - Tự động hóa Textwrap cho chữ thoại, bọc viền bong bóng mờ 80% (RGBA) tạo không gian nghệ thuật, tránh che khuất hình ảnh 100%.
3. **Giải Pháp Nhất Quán Hình Ảnh (Character Consistency):**
   - Đã biên soạn kiến trúc mẫu `ip_adapter_template.json` trên nền tảng ComfyUI. Tính năng nạp Hạt giống Chân dung (Reference Image Seed) qua IP-Adapter đã được chứng thực là khống chế được AI Image Generator giữ nguyên đường nét (Tóc/Quần áo) trên toàn dải tranh liên tiếp.

## 🛑 Điểm Nghẽn Hiện Tại (Bottlenecks & Issues cho v3.0)

### 1. Tràn Viền Bong Bóng Mù (Blind Speech Bubble Overlap)
- **Vấn đề:** Hiện tại tọa độ Bong bóng thoại chỉ được neo bám tĩnh vào rìa dưới/trên của Bounding Box. Hệ thống Python (Pillow) chưa có mắt nhìn (Computer Vision), do đó nó có nguy cơ dán bóng thoại đè thẳng lên mặt hoặc con mắt của nhân vật bên trong bức ảnh.
- **Đề xuất v3.0:** Tích hợp nhận diện khuôn mặt nhẹ (OpenCV DNN hoặc YOLOv8-face) để tự động quét vùng tọa độ "không chứa gương mặt chính" -> đẩy Speech Bubble vào vùng an toàn (Safety Padding).

### 2. Sự Đắt Đỏ Về Tốc Độ Tải IP-Adapter
- **Vấn đề:** Để giữ nhất quán nhân vật bằng IP-Adapter + ControlNet, GPU sẽ phải gồng gánh tải lượng VRAM tính toán cao gấp đôi. Colab Pro (L4/T4) có thể sẽ bị kéo giãn thời gian sinh 1 Frame từ 15s lên tới 35-40s.
- **Đề xuất v3.0:** Cân nhắc thử nghiệm SDXL Turbo hoặc Flux-Schnell (mô hình phản hồi tức thời chỉ tốn 4 bước xử lý AI) để bù trừ lượng tốc độ hao hụt khi gắn IP-Adapter.

### 3. Vắng Bóng Lưới Kéo Góc Chéo (Diagonal Manga Panels)
- **Vấn đề:** Bảng layout hiện tại vẫn là các khối hộp hình chữ nhật cứng ngắc. Họa sĩ chuyên nghiệp đôi khi đánh dốc viền khung (vát nghiêng) để tạo tốc độ vật lý cho kiếm/súng/cảnh vỡ vụn.
- **Đề xuất v3.0:** Bổ sung thuật toán tạo đa giác (Polygon Draw) bằng Alpha Masking trên Pillow (cắt xéo hình). Tuy nhiên đây là phần mở rộng ít ưu tiên, có thể làm sau.

---
**✅ KẾT LUẬN GIAI ĐOẠN 2:** 
Bộ máy Microservices nay đã được vũ trang đầy đủ: `LLM -> Thuật Toán Chia Lưới -> Sinh Ảnh AI -> Ghép Tranh -> Điền Chữ`.
Chúng ta đã đi từ những bức ảnh rời rạc vô thức ở bản v1.0 trở thành một Dải truyện Webtoon Cuộn Dọc Có Tính Toán ở v2.0. Đề tài luận văn của bạn giờ đã đủ cơ sở cực xịn để quay màn hình Demo chức năng rồi!
