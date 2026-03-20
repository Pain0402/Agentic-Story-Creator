from PIL import Image, ImageDraw, ImageFont
import os
from src.backend.models.layout_schema import WebtoonLayout

class WebtoonStitcher:
    def __init__(self, bg_color=(255, 255, 255)):
        self.bg_color = bg_color
        
    def crop_and_resize(self, img_path: str, target_width: int, target_height: int) -> Image.Image:
        """
        Resize and crop the image to fit EXACTLY into the target bounding box 
        to avoid empty gaps and keep the aspect ratio.
        """
        img = Image.open(img_path).convert("RGB")
        img_w, img_h = img.size
        
        target_ratio = target_width / target_height
        img_ratio = img_w / img_h
        
        # Crop based on ratio
        if img_ratio > target_ratio:
            # Image is wider than target -> crop sides
            new_w = int(target_ratio * img_h)
            offset = (img_w - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, img_h))
        elif img_ratio < target_ratio:
            # Image is taller than target -> crop top/bottom
            new_h = int(img_w / target_ratio)
            offset = (img_h - new_h) // 2
            img = img.crop((0, offset, img_w, offset + new_h))
            
        # Resize to exact target size
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img

    def stitch(self, layout: WebtoonLayout, image_paths: list[str], output_path: str = "./output/final_webtoon.png"):
        """
        Pastes the generated AI images into the calculated layout boxes.
        """
        if len(image_paths) != len(layout.panels):
            print(f"Warning: Number of images ({len(image_paths)}) does not match panels ({len(layout.panels)})!")
            # We'll just stitch what we can
            
        # 1. Create blank canvas
        canvas = Image.new("RGB", (layout.canvas_width, layout.canvas_height), self.bg_color)
        
        # 2. Iterate and paste
        for i, panel_def in enumerate(layout.panels):
            if i >= len(image_paths):
                break
                
            img_path = image_paths[i]
            if not os.path.exists(img_path):
                print(f"File not found: {img_path}")
                continue
                
            b = panel_def.box
            
            # 3. Fit the image perfectly into the box
            fitted_img = self.crop_and_resize(img_path, target_width=b.width, target_height=b.height)
            
            # 4. Paste into Canvas
            canvas.paste(fitted_img, (b.x, b.y))
            
            print(f"Pasted Panel {panel_def.panel_id} at ({b.x}, {b.y})")

        # 5. Save the final Webtoon strip
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        canvas.save(output_path)
        print(f"✅ Final Webtoon Strip saved to: {output_path}")

if __name__ == "__main__":
    from src.backend.agents.layout_agent import LayoutAgent
    
    # Simple simulated test to verify the Stitcher
    # We will pretend the generated dummy image from Task 8 is the same image sent back 4 times
    dummy_img_path = "./output/panel_38811159-5f32-45f4-b030-cf18ccb8b7c8_9_0.png"
    
    mock_panels = [
        {"panel_id": 1, "action_intensity": 1},
        {"panel_id": 2, "action_intensity": 2},
        {"panel_id": 3, "action_intensity": 5},
    ]
    agent = LayoutAgent()
    layout = agent.calculate_layout(mock_panels)
    
    stitcher = WebtoonStitcher()
    # Let's see if the image exists, otherwise create a fake red one
    if not os.path.exists(dummy_img_path):
        os.makedirs(os.path.dirname(dummy_img_path), exist_ok=True)
        Image.new("RGB", (512, 512), color="red").save(dummy_img_path)
        
    image_paths_list = [dummy_img_path, dummy_img_path, dummy_img_path]
    stitcher.stitch(layout, image_paths_list, "./output/final_webtoon_test.png")
