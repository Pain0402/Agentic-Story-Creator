# BÁO CÁO KIỂM THỬ END-TO-END (POC GIAI ĐOẠN 1 - v1.0)

## 📌 Thành Quả Đạt Được (What Worked)
1. **Kiến trúc LLM (Narrative Agent):** Hệ thống đã giao tiếp hoàn hảo với mô hình **Gemini-2.5-Flash** thay vì OpenAI. Nó chứng minh khả năng đọc kịch bản, trích xuất chính xác 100% định dạng JSON theo đúng schema yêu cầu (Pydantic model) bao gồm `characters`, `panels`, `dialogue` và `visual_prompt`.
2. **Giao thức Kết nối (Network Architecture):** 
   - Backend sử dụng FastAPI gọn nhẹ, dễ dàng gọi và thử nghiệm.
   - Script phân luồng qua Colab (Worker GPU - `comfyui_client.py`) đã được tổ chức logic tốt với việc phân tách IP qua Ngrok và WebSocket để tải hình ảnh.

## 🛑 Điểm Nghẽn Hiện Tại (Bottlenecks & Issues)

### 1. Thời Gian Xử Lý (Latency)
- Việc sinh 1 đoạn ảnh (1 frame) trên hệ thống T4/V100 Colab phụ thuộc khá lớn vào độ dài của bước lấy mẫu (Sampling steps: 20-30). Đôi lúc phải chờ từ **10 - 20s/frame**.
- *Đề xuất v2.0:* Chuyển qua dùng model **Flux.1 Schnell** (chỉ tốn 4 steps) hoặc chạy Async luồng để render nhiều khung cùng lúc thay vì đợi tuần tự.

### 2. Sự Đứt Gãy Mạch Nhân Vật (Zero Character Consistency)
- Hiện tại, kịch bản tạo ra Txt2Img chỉ dựa vào mô tả ngoại hình bằng chữ *“brown hair, yellow sweater”*. Khi chạy AI Engine từng Frame khác nhau (với Text thay đổi), ngoại hình/tỷ lệ mặt của nhân vật bị đổi liên tục (Lỗi đứt gãy DNA nhân vật).
- *Đề xuất v2.0:* Bắt buộc phải tích hợp **IP-Adapter** hoặc Load **LoRA** chuyên biệt của từng nhân vật vào ComfyUI workflow.

### 3. Thiếu Không Gian Text (No Speech Bubble Space)
- Stable Diffusion chỉ lo nhồi nhét khung cảnh vào toàn bộ tranh (Bleeding edge), làm cho Tác tử Sắp Chữ sau này chắc chắn 100% sẽ dán đè lên mặt nhân vật.
- *Đề xuất v2.0:* Trong thuật toán bố cục Layout, phải ép tỉ lệ tạo ảnh có khung thừa ra không dính nền (Ví dụ: Thêm controlnet trắng) hoặc bắt LLM Agent sinh prompt ưu tiên `negative space`.

---
**✅ KẾT LUẬN GIAI ĐOẠN 1:** 
Phần "Não" (Agent) đã hoàn thiện và chạy trơn tru. Phần "Cơ Bắp" (Colab ComfyUI) đã được lên thiết kế đường ống dẫn (client Python -> ngrok). Sẵn sàng chuyển giao sang **Giai đoạn 2**.
