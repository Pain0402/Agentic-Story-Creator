# KẾ HOẠCH TRIỂN KHAI DỰ ÁN: ANIMEAI WEBTOON (GIAI ĐOẠN 4 - v4.0)

## 📌 Tổng Quan
- **Mục tiêu:** Xây dựng Cổng giao tiếp API hoàn chỉnh trên Backend và Xây dựng Giao diện ứng dụng người dùng (Frontend Web App). Tiến hành thử nghiệm với người dùng cuối (UAT) và triển khai trên máy chủ thực tế để gõ Luận văn.
- **Loại Dự án:** FRONTEND WEB, RESTFUL API INTEGRATION & DEPLOYMENT.
- **Thời gian dự kiến:** 4 Tuần.

## 🎯 Tiêu Chí Thành Công v4.0
1. Backend có đầy đủ các Endpoint bảo mật, cung cấp dịch vụ Sinh truyện tự động (End-to-End) qua giao thức HTTP (FastAPI).
2. Frontend cho phép Nhập Test Kịch Bản, theo dõi tiến độ sinh ảnh (Progress Bar, Loaders), và xem/chỉnh sửa thành quả truyện.
3. Đóng gói mã nguồn đẩy lên hệ thống Server (Có thể giả lập Localhost để trình chiếu Báo cáo).

## 📋 Phân Rã Nhiệm Vụ (Task Breakdown)

### Tuần 14: Hoàn Tất Cổng Giao Tiếp (Backend API Wrapper)
- ✅ **Task 22:** Đóng gói Cỗ máy (Webtoon Engine) vào API FastAPI.
  - **Agent:** `backend-specialist`
  - **Input:** Class `WebtoonEngine` từ Giai đoạn 3.
  - **Output:** Endpoint `POST /api/v3/generate-webtoon`. Endpoint này sẽ nhận Text Script và điều phối 100% Pipeline chạy ngầm. Sau đó trả về link tới File Webtoon hoàn chỉnh. Tích hợp CORS Middleware cho Web.
  - **Verify:** Gọi Endpoint qua Postman và lấy thành công đường dẫn file Ảnh Cuộn.
  
- ✅ **Task 23:** Phân phối Tệp Tĩnh (Static Files Servings).
  - **Agent:** `backend-specialist`
  - **Input:** Thư mục `/output` chứa ảnh truyện tranh.
  - **Output:** Gắn Router cung cấp truy cập công khai vào file ảnh qua URL tĩnh (VD: `http://localhost:8000/static/webtoon_final.png`). Tránh lộ dữ liệu nhạy cảm thư mục khác.
  - **Verify:** Click vào Link trong Response API hiện ra tấm ảnh Webtoon.

### Tuần 15: Xây Dựng Giao Diện Người Dùng (Frontend)
- ✅ **Task 24:** Khởi tạo Web Client (Next.js / React).
  - **Agent:** `frontend-specialist`
  - **Input:** Khung UI Component hiển thị Textbox, Nút Bấm, Khu vực hiển thị Loading.
  - **Output:** Mã nguồn App chạy cổng `:3000`.
- ✅ **Task 25:** Nối Dây Client - Server.
  - **Agent:** `frontend-specialist`
  - **Input:** Axios/Fetch gọi sang `:8000/api/v3/generate-webtoon`.

### Tuần 16 & 17: UAT & Benchmark Giới Thiệu
- **Task 26:** Mở máy chạy rà soát Human-in-the-Loop & Demo Test.
- **Task 27:** Chốt Luận Văn. Đóng gói mã nguồn & Biểu đồ.
