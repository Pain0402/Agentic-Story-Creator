# Kế Hoạch Nâng Cấp Hệ Thống AnimeAI Webtoon bằng Mã Nguồn Mở (OSS) Chuyên Dụng

**Đối tượng:** Tài liệu nghiên cứu & phát triển (R&D) dành cho Luận văn Thạc sĩ/Kỹ sư.
**Mục tiêu:** Chuyển đổi từ hệ thống "Dàn khung cơ bản" sang hệ thống "Sáng tạo nội dung chuyên nghiệp" đạt chuẩn State-of-the-Art (SOTA).

---

## 1. Giải quyết bài toán Nhất quán Nhân vật (Character Consistency)

Đây là vấn đề lớn nhất của truyện tranh vẽ bằng AI: Nhân vật bị thay đổi diện mạo qua từng khung hình.

### Giải pháp OSS đề xuất: **StoryDiffusion** kết hợp **IP-Adapter-FaceID**
- **Cơ chế:**
    - Thay vì chỉ dựa vào mô tả văn bản (Text Prompt), hệ thống sẽ trích xuất đặc điểm khuôn mặt từ một ảnh gốc (Reference Image) và "tiêm" (inject) vào quá trình khuếch tán của tất cả các khung hình tiếp theo.
    - **StoryDiffusion** cung cấp cơ chế *Consistent Self-Attention*, giúp các khung hình trong cùng một batch có sự liên kết chặt chẽ về bối cảnh và trang phục.
- **Cách tích hợp vào Agent:**
    - **Narrative Agent:** Sẽ không chỉ tạo prompt mà còn tạo một đoạn "Mô tả nhận diện nhân vật" (Character ID).
    - **AI Client (ComfyUI):** Cài đặt Custom Node `ComfyUI-StoryDiffusion` và `IP-Adapter`. Truyền ảnh gốc của nhân vật vào workflow này.

---

## 2. Nâng cấp Bố cục Nghệ thuật (Creative & Generative Paneling)

Thay thế việc chia khung "đều chằn chặn" bằng cách sắp xếp khung tranh có nhịp điệu và ý đồ điện ảnh.

### Giải pháp OSS đề xuất: **Manga Layout Generation (Dựa trên Deep Learning)**
- **Cơ chế:**
    - Sử dụng các mô hình đã được huấn luyện trên hàng chục ngàn trang truyện (như Dataset của Manga109).
    - Mô hình sẽ nhận số lượng Panel từ Narrative Agent và tự động vẽ ra "bản đồ phân bổ" (Layout Map) với các khung to, nhỏ, dài, ngắn khác nhau để tạo kịch tính.
- **Cách tích hợp vào Agent:**
    - **Layout Agent:** Thay vì dùng công thức cộng trừ tọa độ đơn giản, Agent này sẽ gọi một Micro-service chạy Model Layout để lấy tọa độ (x, y, w, h) tối ưu nhất.

---

## 3. Tối ưu Phong cách Webtoon (Style Refinement)

Làm cho ảnh vẽ ra không chỉ là "Ảnh AI" mà phải mang linh hồn của "Webtoon/Manhwa".

### Giải pháp OSS đề xuất: **Webtoon-LoRA** & **ControlNet (Tile/Canny)**
- **Cơ chế:**
    - **LoRA (Low-Rank Adaptation):** Sử dụng các file LoRA chuyên biệt như *Manhwa Style*, *LineArt Style* từ CivitAI để ép SD vẽ theo nét vẽ tay, đổ bóng đặc trưng của truyện tranh Hàn Quốc.
    - **ControlNet:** Dùng mô hình `Canny` hoặc `Lineart` để giữ cho các đường nét của nhân vật luôn sắc sảo, không bị mờ nhòe khi thu phóng.
- **Cách tích hợp vào Agent:**
    - **AI Engine:** Cập nhật Workflow của ComfyUI để tự động load các LoRA tương ứng với thể loại truyện (Hành động, Lãng mạn, Kinh dị).

---

## 4. Bong bóng thoại Thông minh (Intelligent Speech Bubble Placement)

Đặt chữ vào vị trí "vàng" của bức tranh mà không cần can thiệp thủ công.

### Giải pháp OSS đề xuất: **Deep Comic Text Placement (LaText)**
- **Cơ chế:**
    - Thay vì né mặt (Face Detection) bằng OpenCV cơ bản, mô hình này sẽ phân tích toàn bộ bố cục ảnh để tìm ra "vùng không gian chết" (Dead space) - nơi đặt chữ sẽ ít gây ảnh hưởng đến nội dung thị giác nhất.
    - Tự động vẽ "đuôi" (tail) của bóng thoại hướng về phía miệng của nhân vật đang nói.
- **Cách tích hợp vào Module:**
    - **Post-processing Module:** Thay thế logic vẽ hình chữ nhật bo góc hiện tại bằng script gọi model LaText để render bóng thoại vector đỉnh cao.

---

## 5. Lộ trình Triển khai (Implementation Roadmap)

| Giai đoạn | Nhiệm vụ trọng tâm | Công nghệ chủ chốt |
| :--- | :--- | :--- |
| **Giai đoạn 1** | Đồng nhất nhân vật | IP-Adapter / StoryDiffusion |
| **Giai đoạn 2** | Nâng cấp Workflow SD | Webtoon LoRA, ControlNet |
| **Giai đoạn 3** | Tự động hóa Layout nghệ thuật | Layout Generation Models |
| **Giai đoạn 4** | Hoàn thiện Hậu kỳ chuyên nghiệp | AI Bubble Placement |

---

## 6. Lợi ích cho Luận văn (Expected Outcomes)

1. **Tính khoa học:** Thể hiện khả năng nghiên cứu và tích hợp các mô hình SOTA hiện nay vào một hệ thống Agent phức tạp.
2. **Tính ứng dụng:** Sản phẩm đầu ra (Webtoon) có thể cạnh tranh trực tiếp về chất lượng với các sản phẩm vẽ tay cơ bản.
3. **Tính đổi mới:** Giải quyết được các vấn đề kinh điển của AI (Sự nhất quán, Bố cục nghệ thuật, Chèn chữ thông minh).

---
*Tài liệu này được soạn thảo để định hướng cho các bước nâng cấp tiếp theo của dự án AnimeAI Webtoon.*
