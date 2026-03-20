# PHÂN TÍCH CHI TIẾT THÀNH PHẦN 3.1: FRONTEND APPLICATION (ỨNG DỤNG NGƯỜI DÙNG)

## 1. Vai Trò Của Frontend
Trong kiến trúc Agentic, người dùng đóng vai trò là "Nhà sản xuất" (Producer/Human-in-the-loop), không phải là người trực tiếp vẽ. Do đó, Frontend không chỉ là một trang web tĩnh hiển thị kết quả, mà là một **Bảng điều khiển (Dashboard) tương tác thời gian thực** để điều phối và kiểm duyệt kết quả sinh ra từ các Tác tử AI.

## 2. Lựa Chọn Công Nghệ (Tech Stack)
Để đảm bảo tính chuyên nghiệp và khả năng mở rộng trong tương lai:
- **Framework Chính:** `Next.js` (React). Hỗ trợ render phía máy chủ (SSR) tốt và cấu trúc thư mục rõ ràng.
- **Ngôn ngữ:** `TypeScript`. Bắt buộc để định nghĩa chặt chẽ các kiểu dữ liệu kịch bản và thông số khung ảnh, tránh lỗi lặt vặt.
- **Quản lý Trạng thái (State Management):** `Zustand`. Nhẹ hơn Redux, cực kỳ phù hợp để lưu trữ trạng thái của Kịch Bản và Trạng Thái Render của hàng chục khung ảnh cùng lúc.
- **Giao diện (UI/Styling):** `Tailwind CSS` kết hợp với thư viện component `shadcn/ui` để có giao diện hiện đại, tối giản, và chuẩn production.
- **Tương tác Canvas:** Thư viện `Konva.js` hoặc `Fabric.js` hoặc cấu trúc thẻ DIV Drag-n-Drop cơ bản để người dùng có thể cầm chuột kéo/thả vị trí bong bóng thoại.

## 3. Kiến Trúc Các Màn Hình Chức Năng (Screen Architecture)

### 3.1 Màn Hình Quản Lý Dự Án (Workspace/Project Dashboard)
- Danh sách các Chapter truyện đang làm dở.
- Nút "Tạo Chapter Mới".
- Khu vực quản lý **Reference Bank** (Ngân hàng Nhân vật): Nơi tác giả upload hình ảnh các nhân vật chính (Goku, Naruto, v.v.), đặt tên (Tag) cho chúng. Frontend sẽ gửi hình ảnh này lên Backend để chuyển thành Vector/Embeddings cho AI "nhớ" khuôn mặt.

### 3.2 Màn Hình Soạn Thảo (Script Editor View)
Chia đôi màn hình (Split-pane view):
- **Cột Trái (Biên tập viên):** Khung `TextArea` phong phú. Nơi gõ kịch bản truyện. 
- Khi gõ xong, có nút **"Phân Tích Kịch Bản" (Parse Script)**. Frontend gọi API lên Backend (Narrative Agent). Backend trả về JSON.
- Frontend biến JSON này thành một danh sách (List) các thẻ (Cards) bên cột phải thể hiện các Cảnh (Scenes).

### 3.3 Màn Hình Duyệt Bố Cục (Layout Approval View)
- Sau khi có danh sách Cảnh, Frontend vẽ ra một mảng lưới (Grid) dọc trống (chỉ có viền đen, nền trắng). Mỗi viền đen là một khung (Panel).
- Người dùng được quyền kéo cạnh của khung để làm nó to ra hoặc thu nhỏ lại (Override lại quyết định của Layout Agent).

### 3.4 Màn Hình Sinh Ảnh & Chỉnh Sửa (Generation & Human-In-The-Loop Canvas)
Đây là màn hình quan trọng nhất.
- Khi người dùng bấm **"Render All Panels"**, Frontend mở WebSockets hoặc dùng kỹ thuật Long-Polling liên tục hỏi Backend xem tiến độ sinh ảnh.
- Từng khung ảnh hiện ra dần theo chiều kết xuất (tạo cảm giác loading mượt mà).
- **Tính năng Duyệt (Approval):** Dưới mỗi ảnh có 2 nút: `[Duyệt]` và `[Tạo Lại Khung Này (Regenerate)]`. Nếu ảnh bị lỗi 6 ngón tay, người dùng bấm `Regenerate`, Frontend chỉ gửi API yêu cầu tạo riêng ID của khung đó, không ảnh hưởng các khung khác.
- **Sửa Text (Typography Edit):** Lớp ảnh AI sinh ra và Lớp chữ thoại (Bong bóng) được tách thành 2 Layer xếp chồng (Z-index). Người dùng có thể click đúp vào chữ để sửa tiếng Việt nếu OCR nhận nhầm, hoặc cầm bong bóng thoại kéo ra chỗ trống khác.

## 4. Giao Tiếp API Cơ Bản (Integration points)
Frontend không tự chứa logic sinh ảnh. Nó giao tiếp với tầng Backend (Agentic Orchestrator) qua các REST Endpoint chính:
- `POST /api/v1/projects` (Tạo dự án mới).
- `POST /api/v1/characters` (Lưu hình mẫu nhân vật).
- `POST /api/v1/agents/parse-script` (Gọi Agent dịch kịch bản).
- `POST /api/v1/agents/generate-layout` (Gọi Agent phân trang).
- `POST /api/v1/agents/render-panel/{panel_id}` (Gọi Agent vẽ ảnh đơn lẻ - Đây là request tốn thời gian nhất, có thể kéo dài 10-30s).
