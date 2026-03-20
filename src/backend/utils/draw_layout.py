from PIL import Image, ImageDraw, ImageFont
import os
from src.backend.models.layout_schema import WebtoonLayout

class LayoutDrawer:
    def __init__(self, bg_color=(255, 255, 255), box_color=(200, 200, 200), outline_color=(0, 0, 0)):
        self.bg_color = bg_color
        self.box_color = box_color
        self.outline_color = outline_color
        
    def draw(self, layout: WebtoonLayout, output_path: str = "./output/dummy_webtoon.png"):
        # Create a blank white canvas matching the calculated height
        img = Image.new("RGB", (layout.canvas_width, layout.canvas_height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # We can try to load a basic font, or fallback to default
        try:
            # Only works if arial is available on system
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()

        # Draw each panel
        for p in layout.panels:
            b = p.box
            
            # The coordinates for PIL rectangle: [x0, y0, x1, y1]
            rect_coords = [b.x, b.y, b.x + b.width, b.y + b.height]
            
            # Draw the box representing the image panel
            draw.rectangle(rect_coords, fill=self.box_color, outline=self.outline_color, width=3)
            
            # Write Panel ID and Action Intensity in the middle
            text = f"Panel {p.panel_id}\nIntensity {p.action_intensity}\n({p.aspect_ratio})"
            
            # Simple text centering
            # Since textbbox might be different in newer pillow, using textlength or rough estimation
            try:
                # Pillow >= 8.0.0
                left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                tw = right - left
                th = bottom - top
            except AttributeError:
                tw, th = draw.textsize(text, font=font)
                
            tx = b.x + (b.width - tw) / 2
            ty = b.y + (b.height - th) / 2
            
            draw.text((tx, ty), text, fill=(0, 0, 0), font=font)
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        print(f"✅ Layout successfully drawn to {output_path}")

if __name__ == "__main__":
    from src.backend.agents.layout_agent import LayoutAgent
    
    # Run the same mock as before
    mock_panels = [
        {"panel_id": 1, "action_intensity": 1},
        {"panel_id": 2, "action_intensity": 2},
        {"panel_id": 3, "action_intensity": 5},
        {"panel_id": 4, "action_intensity": 3},
    ]
    
    agent = LayoutAgent()
    layout = agent.calculate_layout(mock_panels)
    
    drawer = LayoutDrawer()
    drawer.draw(layout, "output/dummy_webtoon.png")
