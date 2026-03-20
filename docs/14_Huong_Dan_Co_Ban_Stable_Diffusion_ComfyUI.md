# TÀI LIỆU BONUS 6: HƯỚNG DẪN CƠ BẢN VỀ STABLE DIFFUSION, COMFYUI VÀ PHƯƠNG PHÁP ỨNG DỤNG CHO LUẬN VĂN

Nếu bạn chưa từng tiếp xúc với các công cụ tạo ảnh mã nguồn mở như Stable Diffusion hoặc ComfyUI, tài liệu này được thiết kế để cung cấp những kiến thức nền tảng vững chắc và cách chúng ghép nối vào hệ thống tác tử của bạn.

---

## 1. Stable Diffusion (SD) Là Gì?
Hiểu đơn giản, Stable Diffusion là một cỗ máy (Mạng nơ-ron học sâu) dùng để chuyển đổi **Văn bản mô tả (Text Prompt)** thành **Hình ảnh (Image)**. Khác với Midjourney hay DALL-E là một dịch vụ web trả phí khép kín, SD là *mã nguồn mở*. Điều này có nghĩa bạn có thể tải lõi (core) thuật toán của nó về chạy ngầm (offline) hoàn toàn trên máy tính cá nhân nếu cấu hình đủ mạnh.

Đặc điểm của Stable Diffusion:
- Không bị giới hạn kiểm duyệt (censorship) nếu dùng mẫu tự host.
- Khả năng tinh chỉnh siêu sâu bằng cách bổ sung các lớp (layer) can thiệp như ControlNet hay LoRA.

**Trong Dự án bạn:** SD sẽ là động cơ chính (Engine) cho "Consistent Generation Agent". Nó giống như một "họa sĩ bị mù", chỉ có thể vẽ khi nghe bạn đọc lệnh prompt truyền xuống từ Tác tử Phân tích (Narrative Agent).

---

## 2. Các Framework Giao Diện Tương Tác: Tại Sao Chọn ComfyUI?

Lõi (Core Python code) của Stable Diffusion khá khô khan. Do đó, cộng đồng nguồn mở viết ra các Giao diện người dùng (Web UI) hỗ trợ click và nhấp thay vì gõ dòng lệnh. Hai loại phổ biến nhất:
1. **Automatic1111 (A1111) / Forge:** Giao diện đơn giản dạng các ô Textbox. Dễ dùng để test ban đầu.
2. **ComfyUI:** Giao diện dạng Nút nối ghép (Node-based workflow). Trông chằng chịt như bản đồ nhưng hiện đang là công cụ TỐT NHẤT THẾ GIỚI.

**Vì sao luận văn này khuyên chọn ComfyUI?**
Bởi vì ComfyUI có cơ chế cực kỳ mạnh: **Lưu lại toàn bộ hệ thống các nút nối dưới dạng mã lệnh JSON**.
- *Cách bạn dùng:* Mở giao diện ComfyUI, kéo xếp các khối Nút để mô hình hóa toàn bộ chuỗi: Đưa kịch bản -> Dùng IP-Adapter mượn nhân vật gốc -> Bật ControlNet tạo dáng vẽ khung hình. Sau khi lưu khối này thành file `workflow.json`, bạn có thể lấy Backend Python (Node JS/FastAPI của phần "Agentic Orchestrator") **bơm thẳng text tự động từ kịch bản** vào file `workflow.json` đó và cho ComfyUI chạy nền mà không cần nhìn giao diện.

---

## 3. Các Plugin Hỗ Trợ Đỉnh Cao Dành Riêng Cho Đồ Án Kể Chuyện Nhất Quán (Nên Cài Đặt Trong ComfyUI / Diffusers)

Tạo một hình lẻ khá dễ, nhưng tạo một đoạn truyện dài mà Goku vẫn nhìn giống Goku bộ quần áo đó mới gọi là bài toán "Character Consistency" (Nhất quán nhân vật) mà đề tài cần giải. Đây là bộ ba công nghệ phải áp dụng:

### A. LoRA (Low-Rank Adaptation)
- **Tác dụng:** Huấn luyện trí não cấp tốc. Diffusion gốc không biết Pikachu là gì chẳng hạn. Khái niệm LoRA là bạn bỏ 20 tấm ảnh Pikachu vào train với mô hình gốc trong 15 phút. Bạn ra một file nhỏ (File LoRA, vài chục MB). Nạp file LoRA này vào, mỗi lần ghi `1pikachu` nó sẽ vẽ chính xác. Trong dự án Webtoon, mỗi Nhân vật Tiểu Thuyết có thể là 1 LoRA.

### B. ControlNet (Kiểm Soát Cấu Trúc Khung)
- **Tác dụng:** Ép Diffusion phải vẽ theo một đường nét thô. Nếu "Tác Tử Bố Cục" cung cấp lệnh đánh nhau mà Diffusion lại vẽ hai đứa ngồi yên thì hỏng. Nếu mình có một cái hình dáng cái xương người que (OpenPose), ControlNet sẽ ép mô hình vẽ tạo dáng của người chính xác dựa trên bộ khung xương kia.

### C. IP-Adapter (Bí kíp Nhất quán Số 1 Hiện Nay 2025/2026)
- **Tác dụng:** Giữ nguyên gốc Nhân Vật bằng 1 Tấm Ảnh Cắt (Reference Image). Rất khủng khiếp và tiện lợi hơn LoRA, bạn ném ảnh khuôn mặt nhân vật A vào khối IP Adapter. Sau đó ra lệnh prompt: `Nhân vật này đánh nhau trong quán Bar`. IP-Adapter sẽ hút toàn bộ DNA tóc, quần áo, nét mặt và hòa vào tấm hình mới mà không cần train mô hình mất thời gian. Tới lúc bảo vệ Đồ án, mang kỹ thuật IP-Adapter ra Demo sẽ đạt điểm rất cao về AI Generative.

---

## 4. Tóm Tắt Quy Trình Bắt Đầu Dành Cho Người Mới
Đừng đi viết code liền, hãy làm quen thuật toán với thao tác kéo thả trước. Ở khâu R&D:

1. **Tuần 1-2:** Mở Google Colab, tìm kiếm từ khóa `"ComfyUI Colab Notebook"` trên Google, và click nút chạy. Giao diện Web xuất hiện.
2. Bạn tải một cặp Checkpoint vẽ Anime về ném vào thư mục Models của ComfyUI (VD: `Animagine XL` từ web hít ảnh *civitai.com* hoặc Hugging Face).
3. Tập tạo các "Node" kết nối: Kéo Node Load Model -> Nối sang Node Text Prompt -> Nối sang Node KSampler (hạt sinh ảo) -> Nối ra Node Save Image. Căn bản là luồng điện đi từ từ trái sang phải.
4. Nắm được luồng, bạn Save lại ở dạng `Developer API JSON Format`. Lúc đó, bạn chính thức sẵn sàng đưa phần cứng này ghép với Backend LLM Agentic.
