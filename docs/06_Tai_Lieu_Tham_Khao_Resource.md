# TÀI NGUYÊN VÀ TÀI LIỆU THAM KHẢO CHO DỰ ÁN

Đây là bộ sưu tập các bài báo học thuật cốt lõi (Papers), kho lưu trữ mã nguồn mở (Open-source Repositories), các sản phẩm thực tế và bộ dữ liệu sẽ là kim chỉ nam cho việc phát triển tác tử Webtoon của bạn.

## 1. Bài Báo Học Thuật Đỉnh Cao (Research Papers)
*(Bắt buộc xem xét để trích dẫn vào phần Reference của Báo cáo Luận văn)*

1. **StoryAgent: Customized Storytelling Video Generation via Multi-Agent Collaboration (2024-2025)**: Một khung làm việc chuẩn mực về việc chia nhỏ quy trình thiết kế, kịch bản tiếng, và bố cục cho hệ thống đa tác tử LLM. Cực kỳ sát với phần "Cơ chế phân cấp Tác tử" của đề tài. (Mã: arXiv:2411.04925).
2. **One missing piece in Vision and Language: A Survey on Comics Understanding (2024)**: Giúp nắm rõ đặc thù dữ liệu truyện tranh. Đặc biệt quan trọng cho việc xây dựng Tác tử Sắp chữ (Typography Agent). (Mã: arXiv:2409.09502).
3. **Collaborative Comic Generation: Integrating Visual Narrative Theories (2024)**: Nghiên cứu áp dụng "Ngữ pháp Tự sự Trực quan", hướng dẫn thuật toán chia khung Webtoon không bị nhàm chán và tuân theo "dòng chảy mắt".
4. **Advances in Artificial Intelligence: A Review for the Creative Industries (2025)**: Báo cáo vĩ mô về sự thay đổi giữa sáng tạo ảnh tĩnh truyền thống và luồng công việc tự động qua Agent AI (arXiv:2501.02725).
5. **Panel-by-Panel Souls: A Performative Workflow for Expressive Faces in AI-Assisted Manga Creation (2025)**: Công trình nghiên cứu xử lý biểu cảm gương mặt thông qua quy trình Performative Mapping.
6. **Understanding How Viewers Perceive AI-Driven Systems (2026)**: Phân tích tâm lý tiếp nhận hình ảnh AI và tính nhất quán hình ảnh để ứng dụng cho tiêu chí UAT kiểm thử (ResearchGate).
7. **ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models (Zhang et al.)**: Paper nền tảng định hình thuật toán tạo dáng xương khớp OpenPose mà chúng ta áp dụng ở tầng Layout Generation.
8. **IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models**: Bí kíp kỹ thuật đằng sau "Reference Component" - dùng để giữ tính nhất quán nhân vật qua các tấm hình (Character Consistency).
9. **MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework**: Cung cấp lý luận làm nền tảng tổ chức các tác tử mô phỏng vai trò (Writer, Editor, Reviewer) nói chuyện với nhau ở Backend.
10. **Agentic RAG for Generative AI (NVIDIA Nemotron 2025)**: Ý tưởng dùng cơ sở dữ liệu Vector lưu trữ "Tiểu sử / Danh tính" nhân vật hỗ trợ Tác tử đọc kịch bản hiểu nhanh các bộ tiểu thuyết cực dài.

## 2. Mã Nguồn Mở Và Thư Viện (Open-source Repositories)
- **LangChain / LangGraph (Python)**: Thư viện bắt buộc để dựng "Não bộ" điều phối các Agent. LangGraph có tính năng rẽ nhánh và lặp (Feedback loops).
- **AutoGen (Microsoft)**: Framework cho phép nhiều Agent giao tiếp với nhau để giải quyết lỗi logic (Cascading errors).
- **HuggingFace Diffusers**: Code mẫu lõi sinh ảnh tạo môi trường Worker Node Python. 
- **ComfyUI**: Công cụ GUI cấu hình JSON API trực quan siêu mạnh cho AI ảnh.
- **YOLOv8 by Ultralytics**: Phân vùng và phát hiện vật thể an toàn để đánh dấu làm chỗ ghép Typography tự động.

## 3. Sản Phẩm Tương Tự (SaaS Products) Để Tham Khảo UX/UI
- **Drawstory.ai / LlamaGen**: Xem cách họ làm Script Editor chia phân cảnh.
- **Toonsutra 2 (Google AI Studio case-studies)**: Công nghệ về layout cuộn đọc dọc (Webtoon). 
- **Comic Creator AI**: Quan sát tính năng "Reference Character" (Cách họ upload mặt nhân vật mẫu và quản lý nhân vật).

## 4. Bộ Dữ Liệu Tham Khảo (Datasets)
- **Sakuga-42M Dataset / AnimeRun**: Mặc dù chuyên về Video (Hoạt hình), nhưng kho tư liệu thẻ (Tags) rất hữu ích để làm Prompt engineering cho các góc máy (Dutch Angle, Close-up, Wide shot).
- **AnimeText Dataset**: Bộ dữ liệu chứa 4.2 triệu khối chữ truyện tranh. Rất đắt giá dùng để phân tích vị trí đặt chữ (Typography).
