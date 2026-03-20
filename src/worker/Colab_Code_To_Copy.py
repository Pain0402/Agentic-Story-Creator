# ĐÂY LÀ ĐOẠN CODE DUY NHẤT BẠN CẦN COPY VÀ CHẠY VÀO TRONG GOOGLE COLAB
# BẠN ĐÃ ĐẨY FOLDER LÊN GOOGLE DRIVE, VÀ COLAB SẼ TỰ ĐỘNG CHẠY Ở ĐÓ

# 1. KÉO SOURCE CODE TỪ GITHUB CỦA BẠN VỀ COLAB
# Thay thế đường dẫn bằng link repository Github của bạn (VD: https://github.com/Pain0402/...)
!git clone https://github.com/Pain0402/Agentic-Story-Creator.git
import os
os.chdir('Agentic-Story-Creator')

# (Nếu bạn dùng Google Drive thì XÓA 4 dòng trên, và BỎ COMMENT 3 dòng dưới đây)
# from google.colab import drive
# drive.mount('/content/drive')
# os.chdir('/content/drive/MyDrive/AnimeAI-Webtoon-Pipeline')

# 2. CÀI ĐẶT OLLAMA VÀ CHẠY LLAMA3 TRONG NGẦM (BACKGROUND) ĐỂ VIẾT KỊCH BẢN
print("Đang cài đặt Ollama...")
!curl -fsSL https://ollama.com/install.sh | sh

import subprocess
import time
print("Đang khởi động Ollama Server...")
subprocess.Popen(["ollama", "serve"])

time.sleep(4)
print("Đang tải model llama3 (Vui lòng đợi vài phút cho 5GB VRAM)...")
!ollama pull llama3

# 3. CÀI ĐẶT CÁC THƯ VIỆN BACKEND THIẾT YẾU
!pip install langchain-community opencv-python "pydantic>=2.0" "fastapi>=0.100.0" uvicorn python-multipart
!pip install -r src/backend/requirements.txt

# 4. EXPOSE (MỞ KHÓA) NGROK RA CHO FRONTEND LOCAL THẤY PORT 8000
from pyngrok import ngrok, conf
# ĐÂY LÀ CHỖ BẠN CẦN THAY TOKEN NGROK CỦA BẠN VÀO (Lấy trên trang chủ ngrok)
NGROK_AUTH_TOKEN = "NHAP_NGROK_TOKEN_CUA_BAN_VAO_DAY"
conf.get_default().auth_token = NGROK_AUTH_TOKEN

public_url = ngrok.connect(8000).public_url

print("\n" + "="*80)
print(f"🔗 [SIÊU QUAN TRỌNG] HÃY COPY URL DƯỚI ĐÂY:")
print(public_url)
print(f"👉 VÀ DÁN VÀO FILE: frontend/.env.local (Thay cho chỗ NEXT_PUBLIC_API_URL)")
print("="*80 + "\n")

# 5. KHỞI CHẠY SIÊU MÁY CHỦ
print("Đang khởi động The AnimeAI Engine Orchestrator...")
!PYTHONPATH=. python src/backend/main.py
