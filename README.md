# 🎨 AnimeAI Webtoon: Text-to-Webtoon Agentic Pipeline 📖

[![Next.js](https://img.shields.io/badge/Frontend-Next.js-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Stable Diffusion](https://img.shields.io/badge/AI-Stable_Diffusion-purple?style=flat-square)](https://github.com/Stability-AI/stablediffusion)

Hệ thống điều phối các Agent (Tác tử) thông minh để chuyển đổi kịch bản văn bản thô thành truyện tranh Webtoon dạng cuộn dọc hoàn chỉnh. Dự án được phát triển trong khuôn khổ nghiên cứu Luận văn.

---

## 🏗️ Kiến trúc Hệ thống (System Architecture)

- **Workflow Orchestrator (Backend):** FastAPI điều phối luồng dữ liệu giữa các Agent.
- **Narrative Agent (LLM):** Phân tích kịch bản, trích xuất thực thể, viết visual prompt.
- **Layout Agent:** Tính toán hình học dàn trang Webtoon tự động.
- **AI Painter (ComfyUI Engine):** Kết nối Google Colab để vẽ tranh chất lượng cao.
- **Typography Engine (CV):** Nhận dạng khuôn mặt và chèn bong bóng thoại tự động.

---

## 📂 Cấu trúc Dự án (Project Structure)

- `src/`: Mã nguồn Backend (Python FastAPI).
- `frontend/`: Giao diện người dùng (Next.js/Tailwind).
- `docs/`: Tài nguyên báo cáo, nghiên cứu và tài liệu luận văn.
- `resources/`: Font chữ, file cấu hình Workflow AI.

---

## 🚀 Hướng dẫn Cài đặt & Chạy demo

### 1. Chuẩn bị Backend
```bash
cd D:\SUPER_PROJECT\AnimeAI_Webtoon_Thesis
.\venv-3.12\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="."; python src/backend/main.py
```

### 2. Chuẩn bị Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Kết nối AI (Colab)
Mở file Notebook trên Google Colab, chạy ComfyUI và cung cấp link Ngrok mới nhất vào Backend.

---

## 📚 Kế hoạch Phát triển SOTA (Kỳ tới)
- [ ] Tích hợp **StoryDiffusion** để đồng nhất gương mặt nhân vật.
- [ ] Áp dụng **Layout Generation Model** thay thế thuật toán chia khung cứng.
- [ ] Nâng cấp AI để nhận diện cảm xúc giọng nói chèn bong bóng thoại biểu cảm hơn.

---
*Dự án đang trong quá trình tích cực bổ sung và tối ưu hóa.*
