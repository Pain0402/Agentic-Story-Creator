# TÀI LIỆU BONUS 3: HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG VÀ QUẢN LÝ TÀI NGUYÊN BẰNG GOOGLE COLAB / GOOGLE DRIVE

Quản lý một siêu dự án AI đòi hỏi việc chia tải rất thông minh giữa các mô hình lớn đè nặng lên GPU và ứng dụng web nhẹ nhàng phía Frontend. Sử dụng **Google Drive Sync kết hợp cùng Google Colab Pro** là chiến lược "Smart Setup" hoàn hảo.

---

## 1. Phương Thức Phối Hợp Môi Trường Cục Bộ (Local) và Google Drive
**Mục tiêu:** Viết Code linh hoạt ngay trên môi trường quen thuộc ở máy cá nhân (VSCode hoặc Cursor), lưu tự động trên mây, sau đó mượn phần cứng (GPU A100/V100) của Colab để kết xuất ra hình ảnh/LLMs.

**Triển khai:**
1. Mở Cài đặt **Google Drive Desktop** trên máy cá nhân, đảm bảo thư mục dự án trỏ vào ổ đĩa ảo (ví dụ: `G:\My Drive\Colab Notebooks\AnimeAI_Webtoon_Thesis`).
2. Mở trình Editor cục bộ (như VSCode), Add Folder/Workspace hướng đúng vào mục `G:\` này.
3. Mỗi dòng lệnh Python được gõ ra và Save lại, Google Drive sẽ đồng bộ nó lên Cloud trong vòng 3-5 giây. Sự chỉnh sửa và kiểm soát phiên bản (Version Control) được thực thi mà không phụ thuộc lệnh Git Push.

---

## 2. Chiến Lược Giao Tiếp API Giữa Google Colab và Local Machine
*Vấn đề:* Colab sẽ giải quyết cho bạn khâu "Tác tử Đồ họa - AI Engine". Nhưng bạn không thể nhét cái Giao diện Website (React) vào chạy trong Google Colab được. Phải kết nối chúng với nhau như thế nào?

**Cách xử lý bằng Ngrok (Hoặc Cloudflare Tunnels/Localtunnel):**
1. Trên Google Colab Pro, bạn Mount (Gắn) Google Drive để truy cập mã nguồn Backend. 
2. Chạy thư viện ComfyUI / Model Stable Diffusion dưới dạng API Headless (Chỉ gọi lệnh không giao diện).
3. Sử dụng đoạn Script Python sau trên Colab để mở Cổng thông tin ra môi trường công cộng:
```python
from pyngrok import ngrok
# Mở port Backend Server ví dụ 8000 (FastAPI) hoặc 8188 (ComfyUI)
public_url = ngrok.connect(8188)
print("🔗 Truy cập Backend của bạn từ mọi nơi qua API này:", public_url)
```
4. Copy cái URL (ví dụ: `https://abcd-123.ngrok.app`).
5. Vào thư mục làm đồ án `G:\...` mở code Web/React Frontend, cấu hình biến số môi trường `.env` đổi link `API_URL` bằng cái URL ngrok vừa lấy.

Bây giờ bạn code và xem Website trên `http://localhost:3000` (ở máy tính bạn), nhưng khi nhấn nút lệnh "Generate", Localhost sẽ đẩy API bay qua Colab để xử lý, dùng năng lượng của Server Google, sau đó gửi ảnh về trang Web Local của bạn.

---

## 3. Quản Trị Cài Đặt Thư Viện Python (Tech Stack Framework)

Tạo sẵn một file `requirements.txt` trong ổ đĩa ảo để đảm bảo dùng ở Máy nhà hay Máy Colab đều đồng nhất:

**A. Lớp Framework Agent (Não điều phối - Chạy Local hoặc Colab)**
```bash
pip install langchain langchain-openai langgraph pydantic fastapi uvicorn
```

**B. Lớp Engine Tạo Ảnh (Khuyến khích chạy trên Colab GPU)**
```bash
pip install diffusers transformers accelerate xformers
```
- Module `xformers` giúp gia tốc tính toán VRAM rất mạnh, làm tăng đáng kể tốc độ lấy mẫu sinh ảnh.

**C. Lớp Xử Lý Ảnh Thuần Tuý Toán Học (Layout & Typography - Chạy Local hoặc Server)**
```bash
pip install opencv-python Pillow numpy ultralytics
```
- `ultralytics` phục vụ cho mô hình YOLOv8 dùng để phát hiện khuôn mặt tránh việc bong bóng thoại che lấp.

---

## 4. Tóm Tắt Quyền Năng Và Phân Chia Tác Nhiệm
- **Local Workspace (Ổ cứng người dùng):** Gõ code, chạy Frontend Server, phát triển giao diện React/Next.js, thiết kế Typography Algorithm, lên sườn tài liệu Markdown Báo Cáo đồ án luận văn.
- **Google Drive Storage:** Lưu dữ liệu dùng chung (Kịch bản mẫu, JSON file, Checkpoint ảnh nhỏ, LoRA, Reference images characters).
- **Google Colab Pro Engine:** Load model Stable Diffusion siêu lớn (5-10 GB). Liên kết với ngrok tạo API tiếp nhận tín hiệu lệnh. Chịu trách nhiệm tạo hàng chục mảnh Puzzle (Pixel Images) ném trả về Local để gắn khung Webtoon. 
