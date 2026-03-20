import textwrap
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from src.backend.models.layout_schema import WebtoonLayout

class SpeechBubbleDrawer:
    def __init__(self, font_size=20):
        try:
            self.font = ImageFont.truetype("arial.ttf", font_size)
            self.bold = ImageFont.truetype("arialbd.ttf", int(font_size * 1.1))
        except IOError:
            self.font = ImageFont.load_default()
            self.bold = ImageFont.load_default()
            
        # Initialize Haar Cascade for fast face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def detect_faces(self, panel_img: Image.Image) -> list:
        """
        Detect faces in a Pillow Image and return a list of bounding boxes (x, y, w, h).
        """
        try:
            # Convert PIL to cv2 (numpy array)
            cv_img = np.array(panel_img.convert("RGB"))
            # Convert RGB to BGR
            cv_img = cv_img[:, :, ::-1].copy()
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
            return faces
        except Exception as e:
            print(f"Face detection error: {e}")
            return []

    def find_safe_zone(self, faces: list, panel_box: tuple, text_box_w: int, text_box_h: int) -> tuple:
        """
        Calculates a safe zone to place the bubble.
        panel_box: (x, y, width, height) of the image panel.
        faces: list of face bounding boxes (relative to panel's local coordinates).
        """
        p_x, p_y, p_w, p_h = panel_box
        
        # Default fallback: Bottom Left
        best_x = p_x + 20
        best_y = p_y + p_h - text_box_h - 20
        
        if len(faces) == 0:
            return best_x, best_y
            
        # Simple heuristic: Avoid the Y-levels of all detected faces if possible
        # Check Top Left/Right vs Bottom Left/Right
        corners = [
            (p_x + 20, p_y + 20),                               # Top Left
            (p_x + p_w - text_box_w - 20, p_y + 20),            # Top Right
            (p_x + 20, p_y + p_h - text_box_h - 20),            # Bottom Left
            (p_x + p_w - text_box_w - 20, p_y + p_h - text_box_h - 20) # Bottom Right
        ]
        
        best_corner = corners[0]
        max_dist = -1
        
        # We want the corner that is FURTHEST away from any face center
        for cx, cy in corners:
            min_dist_to_any_face = float('inf')
            
            # cx/cy are absolute canvas coordinates, faces are relative to panel
            local_cx = cx - p_x
            local_cy = cy - p_y
            
            # Center of the proposed bubble
            bub_center_x = local_cx + text_box_w / 2
            bub_center_y = local_cy + text_box_h / 2
            
            for (fx, fy, fw, fh) in faces:
                face_center_x = fx + fw / 2
                face_center_y = fy + fh / 2
                
                # Euclidean distance
                dist = ((bub_center_x - face_center_x)**2 + (bub_center_y - face_center_y)**2)**0.5
                if dist < min_dist_to_any_face:
                    min_dist_to_any_face = dist
            
            if min_dist_to_any_face > max_dist:
                max_dist = min_dist_to_any_face
                best_corner = (cx, cy)
                
        return best_corner

    def draw_bubbles(self, image_path: str, layout: WebtoonLayout, narrative_panels: list, output_path: str = "./output/final_webtoon_smart_text.png"):
        """
        Draws dialogue bubbles over the finalized webtoon strip using Smart Face Detection.
        """
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}. Cannot draw bubbles.")
            return

        img = Image.open(image_path).convert("RGBA")
        bubble_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(bubble_layer)
        
        panel_dict = {p.get("panel_id"): p for p in narrative_panels}

        for p_layout in layout.panels:
            b = p_layout.box
            n_panel = panel_dict.get(p_layout.panel_id, {})
            dialogues = n_panel.get("dialogue", [])
            
            if not dialogues:
                continue
                
            # Crop the panel locally to detect faces
            # The canvas coordinates are b.x, b.y, b.width, b.height
            panel_crop = img.crop((b.x, b.y, b.x + b.width, b.y + b.height))
            faces = self.detect_faces(panel_crop)
            
            # Aggregate all dialogue for this panel into one chunk for simplicity
            # (In a real app we might draw separate bubbles, but clustering is fine here)
            full_text = " \n".join([f"{d.get('speaker', '')}: {d.get('text', '')}" for d in dialogues])
            wrapped_text = textwrap.fill(full_text, width=32)
                
            # Measure text size
            try:
                left, top, right, bottom = draw.textbbox((0, 0), wrapped_text, font=self.font)
                text_w = right - left
                text_h = bottom - top
            except AttributeError:
                text_w, text_h = draw.textsize(wrapped_text, font=self.font)
                
            pad = 18
            box_w = text_w + pad * 2
            box_h = text_h + pad * 2
            
            # Smart calculating safe zone avoiding faces
            p_box = (b.x, b.y, b.width, b.height)
            safe_x, safe_y = self.find_safe_zone(faces, p_box, box_w, box_h)
            
            # Draw rounded rectangle bubble
            bubble_box = [safe_x, safe_y, safe_x + box_w, safe_y + box_h]
            draw.rounded_rectangle(bubble_box, radius=20, fill=(255, 255, 255, 240), outline=(0, 0, 0, 255), width=3)
            
            # Draw text inside
            draw.text((safe_x + pad, safe_y + pad), wrapped_text, fill=(0, 0, 0, 255), font=self.font)
                
        final_img = Image.alpha_composite(img, bubble_layer).convert("RGB")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_img.save(output_path)
        print(f"🎯 Smart Text Bubbles (Face-Aware) drawn! Saved to: {output_path}")

if __name__ == "__main__":
    from src.backend.agents.layout_agent import LayoutAgent
    
    mock_panels = [
        {"panel_id": 1, "action_intensity": 1, "dialogue": [{"speaker": "Mia", "text": "Will it avoid my face?"}]},
        {"panel_id": 2, "action_intensity": 2, "dialogue": [{"speaker": "Mia", "text": "Yes, Computer Vision works!"}]},
        {"panel_id": 3, "action_intensity": 5, "dialogue": [{"speaker": "Kai", "text": "AMAZING PIPELINE!"}]},
    ]
    
    agent = LayoutAgent()
    layout = agent.calculate_layout(mock_panels)
    
    drawer = SpeechBubbleDrawer()
    in_file = "./output/final_webtoon_test.png" 
    out_file = "./output/final_webtoon_smart_text.png"
    
    drawer.draw_bubbles(in_file, layout, mock_panels, out_file)
