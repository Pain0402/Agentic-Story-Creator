# CHI TIẾT KIẾN TRÚC HỆ THỐNG PHẦN MỀM

## 1. Tổng Quan Kiến Trúc (High-Level Architecture)
Hệ thống được thiết kế theo mô hình **Client-Server**, ứng dụng kiến trúc **Microservices** (khuyến nghị cho các pipeline AI dài) hoặc tuyến tính dạng **Pipeline Monolithic Backend**. 
Tổng thể hệ thống chia làm 3 cụm (clusters) chính:
1. **Presentation Layer (Frontend):** Ứng dụng Web để tương tác, nhận kịch bản, preview trạng thái và tinh chỉnh.
2. **Orchestration Layer (Backend/Agentic Framework):** Lớp điều phối trung tâm chứa các Tác tử (Agents) quản lý luồng dữ liệu (LangChain/LlamaIndex/AutoGen).
3. **Execution Layer (AI Engine):** Các model chạy nặng về toán và đồ họa (Stable Diffusion, ControlNet, Yolov8, Local/Cloud LLM).

## 2. Luồng Hoạt Động Cốt Lõi (Core Workflow)
**Bước 1: Input Mở đầu.** Người dùng nhập văn bản thô dạng kịch bản vào Frontend (gửi qua API `POST /generate_storyboard`).
**Bước 2: Phân tích Kịch bản (Narrative Agent).** Backend đẩy văn bản qua LLM, phân tách kịch bản thành danh sách biến cố `[Cảnh 1, Cảnh 2]`, với siêu dữ liệu cảm xúc.
**Bước 3: Chia khung Bố cục (Layout Agent).** Thuật toán hình học tính toán diện tích tổng, chia khung tương ứng với `[Cảnh 1, Cảnh 2..]` dựa trên mức độ hành động nặng/nhẹ.
**Bước 4: Sinh ảnh Nhất quán (Consistent Generation Agent).** Mỗi khung ảnh được sinh ra thông qua Stable Diffusion. Nó đọc một Reference Bank (Hình mẫu nhân vật) qua IP-Adapter để đảm bảo áo quần, mặt mũi không bị đổi. Dáng đứng được giới hạn bằng khung Layout và ControlNet.
**Bước 5: Thẩm định (Critic Agent - Vòng lặp phản hồi).** Tác tử soi lại ảnh. Nếu ngón tay biến dạng quá nhiều hoặc có yếu tố NSA, yêu cầu Generation Agent sinh lại khung đó.
**Bước 6: Sắp chữ (Typography Agent).** Bóc tách bong bóng thoại, tìm chỗ trống (Negative space) trong từng khung bằng thuật toán phân vùng, in chữ dạng font Comic dán vào khung.
**Bước 7: Xuất xưởng (Output).** Trả về mảng đường dẫn hình ảnh (URL images) của bản Webtoon ghép nối cho Client tải xuống.

## 3. Chi Tiết Từng Thành Phần (Component Drill-Down)

### 3.1. Frontend Application
- **Công nghệ:** React.js / Next.js, Zustand/Redux, TailwindCSS.
- **Tính năng:**
  - Script Editor (Rich text editor cho biên kịch).
  - Canvas Viewer: Hiển thị kéo thả hoặc preview cuộn dọc kết quả.
  - Partial Regeneration: Request tạo lại duy nhất panel số 3 nếu chưa ưng ý.

### 3.2. Agentic Orchestrator (Backend)
- **Công nghệ:** Python, FastAPI, LangGraph hoặc AutoGen (Microsoft) để thiết lập môi trường hội thoại giữa các agent.
- **Thành phần:**
  - *State Manager:* Lưu trữ toàn bộ object kịch bản (vị trí từng khung, token, vector ID).
  - *Router:* Điều phối request sang các node tương ứng.

### 3.3. AI Engine & Worker Nodes
- **Công nghệ:** PyTorch, Diffusers library (Huggingface), vLLM (nếu tự host mô hình ngôn ngữ).
- **Phân hệ Tạo ảnh:**
  - Base Model: `Stable Diffusion XL` hoặc `Flux.1` (Tuning cho thể loại Anime).
  - LoRA/IP-Adapter: Module nạp nhân vật đầu vào. Truyền trọng số (weights) ngay thời điểm runtime.
- **Phân hệ Thị giác máy tính (CV):**
  - OpenCV: Xử lý mảng ma trận pixel, lấp đầy bong bóng, định vị box chữ.
  - Segment-Anything (SAM): Dùng để xác định khoảng trống làm Typography.

## 4. Cách Triển Khai Xây Dựng (Deployment Strategy)
- **Bước 1 (Dev):** Xây dựng và chạy tất cả trên máy cục bộ (Local) có GPU NVIDIA (VRAM > 16GB) hoặc thuê máy ảo RunPod. Mô hình hóa dưới dạng Jupyter Notebook để kiểm nghiệm từng Tác tử độc lập.
- **Bước 2 (Containerization):** Đóng gói Frontend vào Docker container. Đóng gói Backend API vào Docker container. Đóng gói AI Models Pipeline thành một dịch vụ Worker xử lý hàng đợi (Celery/Redis Queue) vì tạo ảnh Webtoon tốn thời gian, tránh bị Timeout (504).
- **Bước 3 (Cloud Deploy):** Dùng AWS EC2 (g4dn.xlarge chứa GPU) hoặc GCP để deploy Worker Node. Frontend + Backend API nhẹ có thể deploy qua Vercel hoặc Render. Dùng AWS S3 để lưu hình ảnh kết quả.
