# KẾ HOẠCH TRIỂN KHAI DỰ ÁN: ANIMEAI WEBTOON (GIAI ĐOẠN 1)

## 📌 Tổng Quan
- **Mục tiêu:** Xây dựng Proof of Concept (v1.0) chứng minh tính khả thi của việc liên kết LLM Agent (Phân tích kịch bản) và AI Engine (Sinh ảnh) để tạo ra các khung ảnh Webtoon rời rạc từ văn bản thô.
- **Loại Dự án:** MICROSERVICES BACKEND & AI ENGINE.
- **Thời gian dự kiến:** 4 Tuần.

## 🎯 Tiêu Chí Thành Công (Success Criteria)
1. Có thể nhập một kịch bản truyện ngắn (Text) và nhận về một file JSON đã bóc tách ngữ nghĩa.
2. Từ file JSON đó, hệ thống gọi tới Stable Diffusion/Flux để kết xuất thành công ít nhất 3 ảnh rời rạc phản ánh được nhân vật và hành động.
3. Không bắt buộc phải có bố cục lưới (Grid/Layout) cuộn dọc phức tạp ở giai đoạn này.

## 🛠️ Tech Stack Giai Đoạn 1
- **Ngôn ngữ:** Python 3.10+
- **Agent Orchestrator:** LangChain / LangGraph, Pydantic (Định dạng JSON output).
- **Backend API:** FastAPI, Uvicorn (Phục vụ kết nối Local và Colab sau này).
- **AI Engine (Image Generation):** Google Colab Pro, ngrok (tạo đường hầm), ComfyUI API hoặc Diffusers.
- **Mô hình Khuyên dùng:** OpenAI GPT-4o-mini (hoặc GPT-4o) cho LLM; Animagine XL 3.1 cho tạo ảnh Anime.

## 📂 Tổ Chức Thư Mục Dự Kiến (File Structure)
```text
AnimeAI_Webtoon_Thesis/
├── docs/                      # (Đã có) Tài liệu dự án
├── src/                       # Thư mục mã nguồn chính (Sẽ tạo mới)
│   ├── backend/               # FastAPI & Agent Orchestration
│   │   ├── agents/            # Chứa các file Python định nghĩa Agent
│   │   │   └── narrative_agent.py  # Tác tử bóc tách kịch bản
│   │   ├── models/            # Pydantic schema cho Dữ liệu
│   │   ├── utils/             # Các hàm phụ trợ
│   │   ├── main.py            # Entry point FastAPI
│   │   └── requirements.txt   # File cấu hình thư viện
│   ├── worker/                # Chứa scripts chạy trên Colab (AI Engine)
│   │   └── comfyui_client.py  # Script gửi prompt JSON vào ComfyUI qua ngrok
├── data/                      # Thư mục dữ liệu thử nghiệm
│   └── sample_scripts/        # Chứa các file .txt kịch bản truyện ngắn
└── .env                       # Chứa API Keys (OpenAI, Ngrok...)
```

---

## 📋 Phân Rã Nhiệm Vụ (Task Breakdown)

### Tuần 1: Cấu trúc Dự án & Chuẩn bị Dữ liệu
- **Task 1:** Tạo khung thư mục `src/backend`, `src/worker`, và `data`.
  - **Agent:** `project-planner` / `backend-specialist`
  - **Input:** Cấu trúc dự kiến ở trên.
  - **Output:** Thư mục và file rỗng được khởi tạo.
  - **Verify:** Kiểm tra bằng lệnh `ls` cấu trúc thư mục.
- **Task 2:** Khởi tạo môi trường ảo (Virtual Environment) và file `requirements.txt`.
  - **Agent:** `backend-specialist`
  - **Input:** Danh sách thư viện cơ bản (`fastapi`, `uvicorn`, `langchain`, `langchain-openai`, `pydantic`, `python-dotenv`).
  - **Output:** File `requirements.txt` chuẩn chỉnh.
  - **Verify:** Chạy lệnh `pip install -r requirements.txt` không lỗi.
- **Task 3:** Tạo 2 kịch bản mẫu sơ khai.
  - **Agent:** `orchestrator`
  - **Input:** Viết 2 đoạn text txt (1 Slice-of-life, 1 Action) bỏ vào `data/sample_scripts/`.
  - **Output:** 2 file txt.
  - **Verify:** File tồn tại và có nội dung tiếng Anh.

### Tuần 2: Xây Lõi Narrative Parsing Agent
- ✅ **Task 4:** Định nghĩa Pydantic Schemas.
  - **Agent:** `backend-specialist`
  - **Input:** Tài liệu `08_Bonus_Prompt_Engineering...` (cần Pydantic output gồm: số cảnh, nhân vật, hành động, text thoại, visual_prompt).
  - **Output:** Code trong `src/backend/models/schema.py`.
  - **Verify:** Pydantic model compile thành công.
- ✅ **Task 5:** Viết Code Logic cho `narrative_agent.py`.
  - **Agent:** `backend-specialist`
  - **Input:** Schema từ Task 4, System Prompt từ tài liệu 08, kết nối OpenAI API.
  - **Output:** Một hàm nhận tham số chuỗi Text và trả về Object Pydantic/JSON tương ứng.
  - **Verify:** Chạy một script test nạp kịch bản Task 3 và in ra JSON hợp lệ.

### Tuần 3: Xây Bước Đệm API & Khảo sát ComfyUI Colab
- ✅ **Task 6:** Bọc Narrative Agent thành 1 API bằng FastAPI (`main.py`).
  - **Agent:** `backend-specialist`
  - **Input:** Code từ Task 5.
  - **Output:** File `main.py` có chứa Endpoints `POST /api/v1/parse-script`.
  - **Verify:** Khởi động server (uvicorn), dùng cURL hoặc Postman gửi file txt và nhận JSON.
- ✅ **Task 7:** Soạn thảo sổ tay hướng dẫn Colab cho AI Engine.
  - **Agent:** `project-planner`
  - **Input:** Tổng hợp lại cách kết nối Ngrok với ComfyUI từ tài liệu 10 và 14. Viết thành 1 file Jupyter Notebook (`.ipynb`) rỗng có sẵn script.
  - **Output:** File `src/worker/Colab_Environment.ipynb`.
  - **Verify:** File tồn tại. Người dùng có thể upload nó lên GG Colab.

### Tuần 4: Chắp ghép & Báo cáo Điểm nghẽn v1.0
- ✅ **Task 8:** Lập trình Client gọi API ComfyUI (`comfyui_client.py`).
  - **Agent:** `backend-specialist`
  - **Input:** JSON Workflow mẫu do User cung cấp từ việc kéo thả ComfyUI (sau khi đã cài SD). Client sẽ thay đoạn text trong JSON bằng `visual_prompt` sinh ở Task 5 rồi gửi POST đến Ngrok server.
  - **Output:** Script Python nhận text, gửi đi, lưu ảnh rớt về.
  - **Verify:** Chạy script tạo thành công 1 ảnh JPG trên máy Local từ Text Prompt tiếng Anh.
- ✅ **Task 9:** Chạy kiểm thử End-to-End (E2E) và lập Báo cáo.
  - **Agent:** `test-engineer`
  - **Input:** Chạy luồng Gửi kịch bản -> Được JSON -> Gửi JSON qua ComfyUI Client -> Nhận List ảnh.
  - **Output:** Một file `v1_evaluation_report.md` liệt kê lỗi hiện tại (sai lầm nhân vật, thời gian chạy).
  - **Verify:** Kiểm tra thư mục chứa 3 ảnh kết quả và 1 file markdown.

## ✅ PHASE X VERIFICATION (Tiêu chuẩn kiểm duyệt cuối)
- [ ] Chạy pylint check file gốc Python.
- [ ] Đảm bảo keys API nằm trong `.env`, không bị hardcode đẩy lên repository.
- [ ] Backend Server `main.py` chạy ổn định trên cổng 8000.
- [ ] Kịch bản test chạy mượt mà từ Văn bản -> Console In JSON.
