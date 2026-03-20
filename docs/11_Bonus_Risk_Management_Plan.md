# TÀI LIỆU BONUS 4: KẾ HOẠCH QUẢN TRỊ RỦI RO & KHẮC PHỤC LỖI (RISK MANAGEMENT PLAN)

Một luận văn thực tế luôn phải nói về điểm nghẽn và cách khắc phục. Trong luồng hoạt động tự động của nhiều Mô hình AI tạo sinh, khả năng thất bại (Fail) có thể xảy ra bất cứ lúc nào, gây hiện tượng vỡ cả trang truyện. Dưới đây là 3 Rủi ro Lớn Nhất và phương án "Fallbacks" (Giải cứu).

## 1. Rủi Ro Số 1: Hiệu Ứng Gọi Lỗi Dây Chuyền (Cascading Errors)
**Nguyên nhân:** Tác tử Phân tích (Agent 1) hiểu lầm kịch bản trào phúng thành một kịch bản u buồn, truyền "Emotion=Sad" cho Tác tử Bố cục (Agent 2). Agent 2 chia thành một khung ngang dài tĩnh lặng. Agent 3 (Tạo ảnh) sau đó được lệnh "Sad" nhưng đoạn hội thoại (Agent 4) lại là nhân vật đang nhe răng cười mỉa. Đầu ra sẽ là một trang truyện phi logic hoàn toàn.
**Giải pháp (Mitigation):** 
Xây dựng một "Checkpoint Verification" (Chốt chặn kiểm duyệt) giữa Bước 2 và Bước 3.
- LLM Agent "Giám Đốc Nghệ Thuật" (Art Director Agent) sẽ duyệt cặp JSON (Cảnh báo: Lời thoại vui - Cảm xúc buồn là Mâu thuẫn logic) và sinh lại/sửa đổi trước khi đẩy xuống Tác tử Layout tốn tiền vẽ ảnh.

## 2. Rủi Ro Số 2: Lỗi Dị Biến Giải Phẫu (Anatomical Hallucination)
**Nguyên nhân:** Bản chất của thuật toán Khuếch tán (Diffusion) đôi khi vẽ ra 6 ngón tay, mắt lác hoặc tay dính vào tường. Tác tử sẽ không biểu hiện gì và cứ thế mang ảnh lỗi này ghép vào Truyện.
**Giải pháp (Mitigation):**
- Sử dụng mô hình CV phụ trợ: Đưa ảnh qua công cụ phát hiện lỗi giải phẫu (Hand/Face detection).
- *Thực tế hơn cho đồ án:* Thêm tính năng **"Human-In-The-Loop"** (Con người can thiệp) trong Frontend. Thay vì bắt máy tự chữa 100%, cho phép người dùng click đúp vào khung bị lỗi ngón tay và nhấn "Regenerate/Inpaint Panel". Máy sẽ giữ nguyên bối cảnh nhưng vẽ lại bàn tay bị hư, trả kết quả trong 5 giây.

## 3. Rủi Ro Số 3: Tràn Bộ Nhớ Context Ở File Truyện Dài (Context Overflow)
**Nguyên nhân:** Truyện tranh là một chuỗi liên tục. Nếu một Webtoon có 5 Chapter, Chapter 5 có một nhân vật xuất hiện ở Chapter 1. LLM Agent thường có "cửa sổ bộ nhớ" hạn hẹp (4k - 128k tokens). Nó sẽ quên nhân vật này mang áo màu gì hoặc tên là gì.
**Giải pháp (Mitigation):**
- Sử dụng Agentic RAG (Retrieval-Augmented Generation): Khi thiết kế Backend, hãy lưu toàn bộ tiểu sử nhân vật và mô tả thiết kế vào Database Vector (Ví dụ: ChromaDB hoặc Pinecone). 
- Khi dịch một dòng kịch bản "Hoàng tử bước tới", LLM Agent sẽ tự động Query (Tìm kiếm truy vấn) "Quần áo hoàng tử" từ Database, và chèn vào Prompt Tự Động: "1boy, blonde hair, royal cape, red jewel". Điều này giúp máy "nhớ" dai vĩnh viễn dù kịch bản dài 100 ngàn chữ.

## 4. Rủi Ro Số 4: Chi Phí Gọi API Khổng Lồ
**Nguyên nhân:** Quá trình Feedback-Loop (Phản biện) nếu gọi API LLM thương mại liên tục sẽ "đốt" tiền rất nhanh.
**Giải pháp:** 
- Giai đoạn Code/Debug: Xài LMStudio/Ollama chạy LLM bản nhỏ gọn dưới máy Local (Ví dụ model Llama-3-8B hoặc Qwen).
- Giai đoạn Layout/Phân tích: Chọn các model giá cực rẻ hoặc Open source để tối ưu tiền điện năng.
