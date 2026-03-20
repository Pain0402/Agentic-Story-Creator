# PHÂN TÍCH CHI TIẾT THÀNH PHẦN 3.3: AI ENGINE & WORKER NODES (BỘ XỬ LÝ ĐỒ HỌA TRUNG TÂM)

## 1. Vai Trò Của AI Engine
Đây là nơi thực thi các tác vụ tính toán hạng nặng (Heavy GPU computing). Nó thuần túy là các đường ống thao tác với Ma trận Tensor (Tạo ảnh, nhận diện ảnh). Nó không quan tâm đến chuyện "truyện này có nội dung gì", nó chỉ nhận các chỉ lệnh thô (ví dụ: "vẽ cho tao ảnh 800x600 mô tả nhân vật A ở tọa độ B") từ **Agentic Orchestrator** và trả về hình ảnh.

## 2. Lý Do Tách Biệt AI Engine Khỏi Backend
Các mô hình như Stable Diffusion sử dụng VRAM (Video RAM của Card đồ họa). Quá trình xử lý rất nặng và dễ chiếm hết tài nguyên máy tính.
- Nếu gộp chung Core Backend (FastAPI) và AI Engine làm một khối, khi đang render ảnh, Backend có thể bị sập (Crash / Out of memory) khiến giao diện web Frontend bị tê liệt.
- Bằng cách tách biệt thành **Worker Nodes**, chúng ta có thể đặt Backend ở một server rẻ tiền (CPU), và đặt AI Engine ở cụm GPU trên Google Colab hay AWS.

## 3. Công Nghệ & Khung Làm Việc (Frameworks)
Với đề tài tạo Webtoon đòi hỏi ControlNet (kiểm soát tư thế) và IP-Adapter (kiểm soát khuôn mặt), cách tốt nhất hiện nay (2025/2026) KHÔNG phải là tự viết script Python Diffusers từ con số 0, mà nên sử dụng một Engine xử lý Workflow có sẵn và gọi API của nó.

**Sự lựa chọn số 2 tối ưu:**
1. **ComfyUI:** Là một hệ thống dạng nút (Node-based GUI) cực kỳ mạnh mẽ cho Stable Diffusion và Flux. ComfyUI có tích hợp API ngầm định. Bạn thiết lập Workflow (nối các dây node) trên giao diện ComfyUI, lưu nó thành đuôi JSON. Sau đó, AI Engine bản chất chỉ là 1 đoạn code Python ném cái file JSON này vào ComfyUI chạy nền không giao diện (Headless mode).
2. **HuggingFace Diffusers:** Thư viện Python cấp thấp hơn. Dùng viết một file `worker.py` import các class như `StableDiffusionXLControlNetPipeline`. 

## 4. Các Giải Thuật Cốt Lõi Bên Trong AI Engine

### 4.1. Base Model (Mô Hình Nền Tảng)
Để ảnh mang đậm phong cách truyện tranh Anime, chúng ta không dùng model "chụp ảnh thực tế".
- Chọn các file mô hình Checkpoint đã Fine-tune chuyên cho anime: `Animagine XL 3.1`, `Anything V5`, hoặc `Flux.1 Anime`.

### 4.2. Dàn Giáo Nhất Quán Hình Ảnh (Character Consistency Module)
Tác tử Đồ họa ở Backend sinh ra Prompt, nhưng nếu chỉ có Text thì mỗi khung sẽ tạo ra mặt 1 người khác. Workflow ở AI Engine BẮT BUỘC có 2 công cụ tham chiếu bằng Hình Ảnh (Image conditioning):
- **IP-Adapter (Image Prompt Adapter):** Nhận ảnh gốc của nhân vật (từ Reference Bank), trích xuất đặc trưng Embeddings, và hòa trộn vào mô hình Diffusion. Giúp áo quần, màu tóc không bị thay đổi.
- **ControlNet:** Kiểm soát cấu trúc, đường nét, bố cục.
  - *ControlNet OpenPose:* Ép mô hình vẽ đúng tư thế đánh nhau, bay nhảy.
  - *ControlNet Canny / Lineart:* Có thể dùng nếu cần phác thảo (sketch) bố cục trước.

### 4.3. Các Thao Tác Thị Giác Sinh Chữ (Typography Computer Vision)
Đây là một Sub-Worker (Không cần GPU quá xịn, CPU chạy cũng được).
- **YOLOv8 & Segment Anything (SAM):** Engine nhập ảnh Webtoon vừa tạo ra, phân loại các khối (Đây là Nhân vật, Đây là Tóc, Đây là Nền Trời).
- **Thuật toán OpenCV (cv2):** Xác định khoảng cách lớn nhất giữa Nhân vật và Lề ảnh để cấp phát tọa độ `[x, y]` khả thi nhất cho bong bóng thoại. Draw hàm `cv2.ellipse` và `cv2.putText()`.

## 5. Phương Thức Tương Tác Giữa Backend & Worker (Giao Thức Mạng)
- **Kiến trúc Serverless / REST API:** Worker Server (ví dụ chạy trên Google Colab) mở một cổng (Port). Quá trình ngrok giúp đường link local trên Colab trở thành một hàm Web API Public.
- **Quy trình:**
  `Backend (Node 4) -> HTTP POST -> [Colab Worker URL]` chứa `{"prompt": "A boy smiling", "ref_img": "base64_str", "width": 800, "height": 600}`.
- Worker trong Colab tiếp nhận, tính toán trên GPU trong 15 giây.
- Xong việc, Worker trả về Backend dạng chuỗi Base64 của tấm ảnh hoặc tự upload lên Imgur/S3 và trả về link URL Ảnh.
