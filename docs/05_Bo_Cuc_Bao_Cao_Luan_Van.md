# BỐ CỤC BÀI BÁO CÁO LUẬN VĂN (MẪU TÙY BIẾN CHO ĐỀ TÀI AI/AGENTIC)

*Tài liệu này được phát triển dựa trên biểu mẫu của Khoa `form_thesis.md`, tinh chỉnh và mở rộng chuyên sâu nhằm phù hợp đặc thù của một đề tài có hàm lượng nghiên cứu AI cao.*

---

## MỞ ĐẦU
- **Lời cảm ơn**
- **Mục lục**
- **Danh mục đồ thị, biểu bảng và hình ảnh**
- **Danh mục Chữ viết tắt & Thuật ngữ (Glossary)** *(Bổ sung: Rất cần thiết cho các thuật ngữ LLM, RAG, Diffusion, Agentic)*
- **Tóm lược (Abstract):** (Tiếng Anh và Tiếng Việt, tối đa 500 từ). Nêu tóm tắt Bài toán -> Đề xuất Multi-Agent -> Kết quả thực nghiệm đạt được.

## PHẦN GIỚI THIỆU (Chương Mở Đầu)
1. **Đặt vấn đề:** Ngành truyện tranh đang bùng nổ, việc sản xuất Webtoon đòi hỏi thâm dụng lao động. Khó khăn lớn nhất là "Character Consistency" (Nhất quán nhân vật) và Layout.
2. **Những nghiên cứu liên quan:**
   - Các phương pháp Text-to-Image truyền thống (Sora, SD).
   - Điểm yếu của quy trình sinh cảnh tĩnh và vấn đề đứt gãy mạch dẫn truyện.
   - Các hệ thống Framework Storyboard đang có (ví dụ Panel-by-Panel Souls, StoryAgent ...). Từ đó rút ra khoảng trống nghiên cứu (Research Gap).
3. **Mục tiêu đề tài:** Tự động hóa nội dung chuyển từ Kịch bản thành Webtoon 4 lớp (Phân tích, Bố cục, Hình ảnh, Sắp chữ).
4. **Đối tượng và phạm vi nghiên cứu:** Chuyển đổi thể loại truyện ngắn, kịch bản tiếng Anh/Việt. Quản lý đồng thời tối đa N nhân vật.
5. **Phương pháp nghiên cứu:** Phương pháp thực nghiệm, phân tích mô hình, mô phỏng quy trình Agentic.
6. **Nội dung nghiên cứu & Phân công:** Kể cụ thể (Nếu nhóm 2 người: A lo LLM & Backend, B lo Graphic Model & Frontend).
7. **Bố cục của quyển luận văn.**

---

## PHẦN NỘI DUNG

### Chương 1 - Đặc Tả Yêu Cầu Và Phân Tích Bài Toán
1.1. Khảo sát nghiệp vụ: Quy trình biên tập & vẽ Webtoon thực tế (Human workflow).
1.2. Phân tích yêu cầu chức năng:
   - Hệ thống nhập kịch bản.
   - Hệ thống quản lý tài nguyên nhân vật gốc.
   - Trình chỉnh sửa kết quả Webtoon.
1.3. Yêu cầu phi chức năng (Hiệu năng, độ trễ, tài nguyên GPU).
1.4. Đề xuất quy trình làm việc với AI (Agentic Workflow).

### Chương 2 - Cơ Sở Lý Thuyết & Công Nghệ Áp Dụng
2.1. Nền tảng Mô hình Khuếch tán (Diffusion Models - SD, Flux) & Vấn đề tùy chỉnh (ControlNet, IP-Adapter, LoRA).
2.2. Kiến trúc Tác tử AI (LLM Agents) & LangGraph/AutoGen.
2.3. Trí tuệ Thị giác & Phân tách ảnh (SAM, YOLO) áp dụng cho Typography.
2.4. Ngữ pháp Tự sự Trực quan (Visual Narrative Grammar) trong truyện tranh.

### Chương 3 - Thiết Kế Và Cài Đặt Hệ Thống
3.1. Kiến trúc hệ thống tổng quan (Sơ đồ Microservices / Client-Server).
3.2. Cấu trúc và Luồng dữ liệu (Data Flow) giữa các Agents (4-Layer Framework).
   - Narrative Parsing Agent (Thiết kế system prompt).
   - Layout Generation Agent (Giải thuật hình học phân trang).
   - Consistent Generation Agent (Thiết kế pipeline render).
   - Typography Agent (Giải thuật lấp đầy bóng thoại).
3.3. Thiết kế Cơ sở dữ liệu (Schema lưu trữ project, panels, text).
3.4. Mô tả giao diện người dùng UX/UI.

### Chương 4 - Thực Nghiệm Và Đánh Giá (Kiểm Thử)
4.1. Môi trường thực nghiệm (Cấu hình Hardware, Server, Dataset sử dụng).
4.2. Kịch bản kiểm thử:
   - Bài test Nhất quán nhân vật (So sánh chỉ số học máy SSIM/FID).
   - Bài test Sắp chữ (Tỉ lệ che khuất mặt).
4.3. Đánh giá từ người dùng thực tế (User Acceptance Testing - khảo sát ý kiến).
4.4. Đánh giá tính tối ưu thời gian: Thời gian làm bằng người thật so với sử dụng hệ thống. Biểu đồ đánh giá tốc độ hệ thống (FPS sinh ảnh).

---

## PHẦN KẾT LUẬN
- **Kết quả đạt được:** Tóm lược lại giá trị mang lại. Đã giải quyết được bao nhiêu % "Cascading errors".
- **Hạn chế hệ thống:** Hệ thống còn lỗi biến dạng tứ chi (cố hữu của model ảnh), tài nguyên sinh ảnh ngốn phần cứng.
- **Hướng phát triển tương lai:** Khả năng kết nối Agent để xuất thẳng thành Video Animatic, tối ưu hóa real-time rendering.

## TÀI LIỆU THAM KHẢO
*(Chuẩn trích dẫn IEEE / APA, tổng hợp giấy tờ về Agentic, Diffusion).*

## PHỤ LỤC
- Phụ lục A: Hướng dẫn cài đặt môi trường.
- Phụ lục B: Bộ System Prompts gốc của các Agents.
- Phụ lục C: Demo một kịch bản hoàn chỉnh (Trước và Sau khi máy xử lý).
