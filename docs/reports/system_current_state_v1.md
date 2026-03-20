# Báo Cáo Hiện Trạng Phát Triển Hệ Thống AnimeAI Webtoon (v1.0)

**Ngày cập nhật:** 16/03/2026
**Mục tiêu Document:** Tổng hợp toàn bộ kiến trúc, các module đã hoàn thiện và kết quả đạt được của dự án tự động hóa tạo Webtoon từ kịch bản văn bản (Text-to-Webtoon) tính đến thời điểm hiện tại.

---

## 1. Kiến Trúc Hệ Thống Tổng Thể (System Architecture)

Hệ thống đã được xây dựng hoàn chỉnh theo mô hình **Agentic Workflow (Đa tác tử)** và kiến trúc **Client-Server** phân tán (Local Backend + Cloud AI Engine).

- **Frontend:** Next.js (React), TailwindCSS. Chạy tại Local (`localhost:3000`/`3001`).
- **Backend Orchestrator:** FastAPI (Python). Chạy tại Local (`localhost:8000`). Trực tiếp điều phối các luồng Agent.
- **AI Execution Engine:** ComfyUI + Stable Diffusion. Chạy trên **Google Colab (GPU)**, giao tiếp với Backend thông qua đường hầm **Ngrok** (WebSocket/HTTP).

---

## 2. Các Tác Tử (Agents) & Module Đã Triển Khai

Chúng ta đã code và tích hợp thành công chuỗi Pipeline bao gồm 5 Module/Agent cốt lõi:

### 2.1. Narrative Agent (Tác tử Biên kịch)
- **Tệp tin:** `src/backend/agents/narrative_agent.py`
- **Nhiệm vụ:** Đóng vai trò là bộ não ngôn ngữ. Nhận kịch bản thô của người dùng và chuyển đổi thành cấu trúc dữ liệu JSON chặt chẽ (StoryboardSchema).
- **Công nghệ:** LangChain + Google Gemini Generative AI (hiện đang thiết lập dùng `gemini-1.5-flash`).
- **Trạng thái:** Đã hoàn thiện. Tuy nhiên, để linh hoạt trong quá trình test và tránh lỗi Quota Limit (Giới hạn API), hiện tại Agent này đang được dùng **Cơ chế Mock (Fallback)** để tự động trả về kịch bản gồm 2 khung hình mẫu sẵn để luồng chạy không bị gián đoạn.

### 2.2. Layout Agent (Tác tử Dàn trang)
- **Tệp tin:** `src/backend/agents/layout_agent.py`
- **Nhiệm vụ:** Tính toán toán học không gian 2D. Tự động tính toán chiều cao tổng Canvas và tọa độ (Bounding Boxes : X, Y, W, H) cho từng khung tranh dựa trên số lượng panel.
- **Trạng thái:** Đã hoạt động tự động 100%.

### 2.3. ComfyUI Client (Thợ máy AI)
- **Tệp tin:** `src/worker/comfyui_client.py`
- **Nhiệm vụ:** Kết nối từ xa tới máy chủ Google Colab. Nhận các `visual_prompt` từ Narrative Agent, ép vào Workflow JSON của ComfyUI, gửi đi và chờ nhận lại hình ảnh `.png` chất lượng cao.
- **Điểm nhấn:** Đã tích hợp tính năng tự động chuẩn hóa URL (bỏ `https://`) và kết nối thành công qua Ngrok Bypass.
- **Trạng thái:** Kết nối mượt mà, trả ảnh thành công.

### 2.4. Stitching & Speech Bubble (Hậu kỳ & Chữ)
- **Tệp tin:** `src/backend/utils/stitching.py`, `src/backend/utils/speech_bubble.py`
- **Nhiệm vụ:** Nhận hình ảnh lẻ rời rạc từ Colab, ghép lại thành dải Webtoon cuộn dọc. Đồng thời dùng **OpenCV** để phát hiện vị trí khuôn mặt nhân vật, từ đó né mặt ra và vẽ tự động các khung chứa text (Speech Bubble) rồi chèn đoạn thoại vào.
- **Trạng thái:** Hoạt động tốt, hoàn thiện chu trình End-to-End.

### 2.5. Critic Agent (Tác tử Giám khảo - Đang ẩn)
- **Tệp tin:** `src/backend/agents/critic_agent.py`
- **Nhiệm vụ:** Dùng LLM Vision để chấm điểm ảnh xuất ra, nếu lỗi (méo mó, sai prompt) sẽ bắt vẽ lại.
- **Trạng thái:** Code đã hoàn thiện 100%, nhưng đang **tạm thời Tắt (Disabled)** trong vòng lặp của Engine để né việc đánh API quá nhiều gây cạn kiệt Quota free.

---

## 3. Thành Tựu & Cột Mốc Đạt Được (Milestones)

1. **Khắc phục triệt để lỗi System/Môi trường:** Đã chuyển toàn bộ dự án từ Google Drive sang ổ đĩa Local (`D:\SUPER_PROJECT\`) thành công, khởi tạo lại môi trường `venv` tĩnh, gỡ bỏ triệt để các rào cản I/O của Google Drive.
2. **Khắc phục lỗi Frontend - Backend:** Đã chuyển đổi chuẩn xác mô hình API từ Bất đồng bộ (`async def`) sang luồng chạy đồng bộ trong Threadpool (`def` thuần), giúp FastAPI **không còn bị đóng băng (Freezing)** khi gọi Request mô hình nặng.
3. **End-to-End Pipeline Success:** Hệ thống đã chạy thành thông luồng dữ liệu toàn tuyến. Minh chứng là bức ảnh `webtoon_65599f61_final.png` đã được sinh ra, ghép lại 2 khung hình, và có in thoại hoàn chỉnh mà không gặp đứt gãy giữa chừng.

---

## 4. Các Hạn Chế Hiện Tại (Điểm Yếu)

1. **Phụ thuộc API ngặt nghèo:** Hệ thống vướng rào cản tỷ lệ Giới hạn (Rate Limit) rất cứng của Google API (Gemini). Việc test liên tục cần tiền năng hoặc nhiều tài khoản mô phỏng.
2. **Thiếu sự tinh tế trong Layout:** Mặc dù ghép mượt mà, nhưng Layout tính toán vẫn là các khung ngang vuông vức (Panel chia đều tĩnh), thiếu tính nghệ thuật (các khung chéo, lồi lõm) của một Webtoon tiêu chuẩn.
3. **Thiếu sự tự nhận thức hình học bong bóng thoại:** Việc nhận diện khuôn mặt bằng OpenCV là cơ bản, thỉnh thoảng bóng thoại (Speech bubbles) bị dàn hàng ngang cứng nhắc chứ không linh hoạt.
4. **Nhân vật chưa nhất quán (Consistency):** Khi tạo nhân vật từ xa với Stable Diffusion cơ bản, chưa có cấu trúc duy trì khuôn mặt cố định qua nhiều khung kịch bản phức tạp.

---

## 5. Đề Xuất Phát Triển Tiếp Theo (Dành cho Cải tiến Core Thesis)

Để nội dung Đồ án / Luận văn trở nên "Cao cấp" (State-of-the-Art) hơn và ghi điểm, chúng ta cần dần dần thay thế các giải pháp cơ bản bằng các mã nguồn mở tối ưu hơn:
- 💡 Thay thế prompt thuần bằng kỹ thuật **StoryDiffusion** để **Đảm bảo tính nhất quán của thiết kế nhân vật**.
- 💡 Tích hợp các quy tắc **Dàn trang Manga/Webtoon tự động (Generative Paneling)** thay vì toán học tuyến tính.
- 💡 Phát triển giao diện cho phép người thiết kế (User in the Loop) ở Frontend được phép can thiệp thủ công (chỉnh sửa text, đổi vị trí bóng thoại) trước khi chốt hạ tấm hình cuối cùng.
