# TÀI LIỆU BONUS 1: HƯỚNG DẪN PROMPT ENGINEERING CHO CÁC TÁC TỬ (MULTI-AGENT PROMPTS)

Sự thành bại của một kiến trúc "Agentic" nằm trọn ở System Prompts – cách bạn chỉ thị cho các mô hình Ngôn ngữ/Ảnh đóng dung đúng vai trò thực hiện công việc. Đề tài áp dụng tiếng Anh chuẩn để chặn hiện tượng bịa đặt (hallucination) và tương thích hoàn toàn với các chuẩn API thế giới.

## 1. System Prompt Đối Với: Narrative Parsing Agent (Tác Tử Phân Tích Kịch Bản)
**Role:** Bạn là một Tổng Biên Tập Truyện Tranh Webtoon đầy kinh nghiệm. Nhiệm vụ của bạn là bóc tách kịch bản, chia luồng hợp lý.
*Ngôn ngữ gửi vào LLM API:*
```text
You are an expert Webtoon Storyboard Editor. I will provide you with a raw story script. 
Your rigid objective is to break down this script into optimal comic vertical panels.
Follow these rigid rules to output ONLY the required JSON format:

1. Identify character names, minimal visual tags, and current emotions.
2. Break the text into sequences, assigning 'action_intensity' from 1 (calm, dialogue heavy) to 5 (explosive, action, climax).
3. Summarize complex dialogue into brief snippets suitable for speech bubbles.
4. Construct a 'visual_prompt' describing the scene, camera angle, character action focusing heavily on descriptive visual cues (Danbooru styling).

Return ONLY valid JSON.
```

**Ví dụ Format Đầu Ra Kỳ Vọng (JSON từ Output Parser):**
```json
{
  "total_panels": 3,
  "characters": [{"name": "Akira", "tags": "boy, black messy hair, school_uniform"}],
  "panels": [
    {
       "panel_id": 1,
       "action_intensity": 1,
       "visual_prompt": "Close-up of Akira's face, tired and exhausted expression, looking out the window, sunlight shining in classroom, masterpiece, detailed",
       "dialogue": [{"speaker": "Akira", "text": "Today is so exhausting..."}]
    },
    ...
  ]
}
```

## 2. Kỹ Thuật Viết Prompt Ảnh Cho: Consistent Generation Agent (Tác Tử Đồ Họa)

Việc viết prompt (hướng dẫn hình ảnh) cho AI như Stable Diffusion mảng Anime cần sử dụng các Tag đặc tả tĩnh (Danbooru style). Tác tử Backend của bạn sẽ nối các biến (variables) lập trình lại thành 1 chuỗi.

**Standard Positive Prompt Template System:**
```python
positive_prompt = f"masterpiece, best quality, ultra-detailed, webtoon style, comic format, {panel.visual_prompt}, {character.reference_tags}, cinematic lighting, dynamic angle, vibrant colors"
```

**Standard Negative Prompt System (Ràng buộc triết tiêu rác):**
```python
negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, speech bubble, dialog lines, multiple views"
```
*(Đặc biệt chú ý từ khóa `text` và `speech bubble` ở trên để triệt tiêu hiện tượng Mô hình AI tự ý chèn mớ chữ bậy bạ vào trong bức vẽ, giúp "Typography Agent" rảnh tay thao tác chèn bong bóng chữ việt ở đoạn sau).*

## 3. System Prompt Đối Với: Critic / Reflection Agent (Tác Tử Phản Biện & Sửa Lỗi Ngoại Lệ)
**Role:** Rà soát kiểm tra mâu thuẫn hệ thống trước khi Render đồ họa tốn kém. Dùng mô hình giá rẻ như Llama3-8B hoặc gpt-4o-mini thực thi chốt chặn phản hồi (Feedback Loop).

*Ngôn ngữ gửi vào Critic LLM API:*
```text
You are a Quality Assurance Engine for an automated comic generation pipeline.
You will be provided with:
1. The original script.
2. The parsed JSON panel sequence produced by the Narrative Agent.

Your task is to review and point out logical contradictions. Evaluative criteria:
- Does the 'action_intensity' match the actual sentiment of the scene?
- Are too many dialogues cramped into one single panel?
- Is there any hallucinated character that wasn't present in the original script?

Score the JSON file from 1 to 10. If the score is > 8, output "[PASS]". If score <= 8, output "[REJECT]: {Reason for failure, required changes for regeneration}".
```

---
*Mẹo Thực Hành (Programming Tip):* Sử dụng **LangChain PydanticOutputParser** hoặc tính năng **Structured Outputs** của OpenAI API trong Python để ép mô hình trả chuẩn JSON 100%, bảo đảm không có tỷ lệ hỏng (fail rate) trên đường ống Agentic.
