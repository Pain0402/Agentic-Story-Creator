# PHÂN TÍCH CHI TIẾT THÀNH PHẦN 3.2: AGENTIC ORCHESTRATOR (BACKEND ĐIỀU PHỐI)

## 1. Vai Trò Của Orchestrator
Nếu AI Engine là "Cơ bắp", thì Agentic Orchestrator chính là "Bộ não". Tầng này không trực tiếp chạy mạng nơ-ron sinh ảnh nặng nề, mà nó quản lý **luồng công việc (Workflow/Pipeline)**. Nó ra lệnh cho AI Text (LLM) trích xuất dữ liệu, định tuyến (Route) dữ liệu đó cho AI Sinh ảnh, lấy ảnh về, đưa cho modul Python OpenCV dán chữ, và gom thành phẩm trả cho Frontend.

## 2. Lựa Chọn Công Nghệ (Tech Stack)
- **Framework API:** `FastAPI` (Python). Cực kỳ nhanh, hỗ trợ xử lý bất đồng bộ (Async) - bắt buộc phải có vì các tác vụ AI thường có thời gian chờ lâu.
- **Framework Agentic:** `LangGraph` (thuộc hệ sinh thái LangChain) hoặc `AutoGen`. `LangGraph` dạo gần đây (2025/2026) được ưa thích hơn vì nó cho phép bạn định nghĩa các luồng Agent dưới dạng Đồ thị trạng thái (State Graph), giúp quản lý các vòng lặp (Feedback loops) rất dễ.
- **Cơ sở dữ liệu Vector (Vector DB):** `ChromaDB` (chạy local, nhẹ) hoặc `Pinecone` (Cloud). Dùng làm "Bộ nhớ dài hạn" để AI nhớ các đặc điểm nhân vật.
- **Cơ sở dữ liệu thông thường:** `PostgreSQL` hoặc `MongoDB` để lưu thông tin tài khoản, project, kịch bản gốc.

## 3. Cấu Trúc Đồ Thị Tác Tử (Agentic Graph Design)

Trong LangGraph, ta định nghĩa một `State` cục bộ lưu trữ `script_text`, `panels_data`, `images`. Các Tác tử (Nodes) sẽ thay phiên nhau sửa đổi `State` này.

### Node 1: Narrative Agent (Tác tử Kịch Bản)
- **Nhiệm vụ:** Gọi API LLM (GPT-4o hoặc Claude 3.5).
- **Hoạt động:** Nạp `script_text`. Sử dụng System Prompt chuyên dụng (quy định bằng Tiếng Anh) ép LLM trả về JSON có cấu trúc Pydantic strict.
- **Kết quả:** Trả ra `list[Panel]` (Gồm lời thoại, mô tả hành động, danh sách nhân vật).

### Node 2: Memory/RAG Agent (Tác tử Bộ Nhớ)
- **Nhiệm vụ:** Tìm kiếm đặc tính nhân vật.
- **Hoạt động:** Duyệt qua danh sách nhân vật từ Node 1. Lên ChromaDB truy vấn xem "Nhân vật A" này mặc đồ màu gì. Gộp thông tin đó vào `visual_prompt`.

### Node 3: Layout Agent (Tác tử Bố Cục)
- **Nhiệm vụ:** Chia lưới hệ tọa độ.
- **Hoạt động:** Chạy thuật toán lập trình thuần túy (Toán hình học). Tính `Width=800`, tùy biến `Height` dư dúa vào `action_intensity`. Trả ra danh sách `[x, y, width, height]` cho từng phần.

### Node 4: Generation Router (Trạm Điều Phối Đồ Họa)
- **Nhiệm vụ:** Đẩy lệnh sang Server GPU (AI Engine).
- **Hoạt động:** Gọi HTTP Request tới cái API của thằng Worker Node (ví dụ `http://gpu-worker:8188/prompt` của ComfyUI). Nó phải ở dạng Async Task để không làm treo Backend.
- **Kỹ thuật bắt lỗi:** Thường xuyên Ping kiểm tra xem Worker vẽ xong chưa. Lấy URL ảnh về gán vào `State`.

### Node 5: Critic / Reflexion Agent (Tác tử Kiểm duyệt & Vòng lặp)
- **Nhiệm vụ:** Đánh giá chất lượng.
- **Hoạt động:** (Tùy chọn cho phiên bản v3.0). Đưa ảnh vừa sinh từ Node 4 cho một LLM Đa phương thức (Vision LLM) hoặc YOLO. Hỏi "Có 6 ngón tay không?". Nếu "Có", LangGraph tự động kích hoạt một luồng móc ngược (Edge) về Node 4 yêu cầu vẽ lại. Nếu "Không", đi tiếp.

### Node 6: Typography Agent (Tác tử Sắp Chữ)
- **Nhiệm vụ:** Đóng gói hoàn thiện.
- **Hoạt động:** Chạy modul Python OpenCV, nhận ảnh từ Node 4, nhận tọa độ Text trống, dán bong bóng và chữ (từ Node 1) lên ảnh.

## 4. Quản Lý Trạng Thái (Task Queue)
Bởi vì quá trình từ Node 1 -> Node 6 có thể mất từ 1 đến 5 phút, Backend không thể giữ kết nối HTTP treo với Frontend.
Kỹ thuật ở đây là:
1. Frontend gởi POST. Backend tạo một `task_id = 999`, đưa vào hàng đợi `Celery` hoặc `Redis Queue`, và lập tức trả về `{"status": "processing", "task_id": 999}`.
2. Quá trình langGraph chạy ngầm ở Background.
3. Frontend dùng phương pháp Polling (gọi GET 3 giây 1 lần) hoặc WebSockets để nhận phần trăm (%) hoàn thành từ `task_id` này.
