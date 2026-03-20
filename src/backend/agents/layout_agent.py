from typing import List, Dict, Any
from src.backend.models.layout_schema import WebtoonLayout, LayoutPanel, BoundingBox

class LayoutAgent:
    def __init__(self, default_width=800, margin_x=30, base_margin_y=80, gutter=20):
        """
        Uses an algorithmic approach (Visual Narrative Grammar) with clustering.
        Rules:
        - Consecutive panels with low intensity (1-2) can be placed side-by-side (2 columns) 
          to simulate traditional comic grids on a webtoon format if they fit.
        - Intensity 3 -> Full width 3:4 aspect ratio, normal spacing.
        - Intensity 4-5 -> Full width 9:16 or larger, massive vertical spacing for scroll impact.
        """
        self.W = default_width
        self.MX = margin_x
        self.MY = base_margin_y
        self.internal_w = self.W - (self.MX * 2)
        self.gutter = gutter

    def calculate_layout(self, narrative_panels: List[Dict[str, Any]]) -> WebtoonLayout:
        panels_out = []
        current_y = 50 # Start padding top

        i = 0
        n = len(narrative_panels)
        
        while i < n:
            p = narrative_panels[i]
            intensity = p.get("action_intensity", 1)
            p_id = p.get("panel_id", i+1)
            
            # Check if we can cluster 2 low-intensity panels side-by-side
            if intensity <= 2 and i + 1 < n and narrative_panels[i+1].get("action_intensity", 1) <= 2:
                # Pair found: place them side-by-side
                p2 = narrative_panels[i+1]
                p2_id = p2.get("panel_id", i+2)
                p2_intensity = p2.get("action_intensity", 1)
                
                half_w = (self.internal_w - self.gutter) // 2
                
                # Height of a square or slight rectangle for paired panels
                h = int(half_w * 4 / 3) # 3:4 vertical rectangle for side-by-side

                # Panel 1 (Left)
                panels_out.append(LayoutPanel(
                    panel_id=p_id,
                    action_intensity=intensity,
                    box=BoundingBox(
                        x=self.MX,
                        y=current_y,
                        width=half_w,
                        height=h
                    ),
                    aspect_ratio="3:4"
                ))

                # Panel 2 (Right)
                panels_out.append(LayoutPanel(
                    panel_id=p2_id,
                    action_intensity=p2_intensity,
                    box=BoundingBox(
                        x=self.MX + half_w + self.gutter,
                        y=current_y,
                        width=half_w,
                        height=h
                    ),
                    aspect_ratio="3:4"
                ))

                current_y += h + self.MY
                i += 2
                continue

            # Standard Full-Width Placement
            if intensity <= 2:
                # 16:9 widescreen or standalone horizontal
                h = int(self.internal_w * 9 / 16)
                aspect = "16:9"
                spacing = self.MY
                
            elif intensity == 3:
                # 1:1 Square
                h = self.internal_w
                aspect = "1:1"
                spacing = int(self.MY * 1.5)
                
            else: 
                # 4-5: Intense Action / Emotional Climax -> 9:16 Vertical
                h = int(self.internal_w * 16 / 9)
                aspect = "9:16"
                spacing = self.MY * 3  # Lots of dramatic sliding space!

            box = BoundingBox(
                x=self.MX,
                y=current_y,
                width=self.internal_w,
                height=h
            )

            panels_out.append(LayoutPanel(
                panel_id=p_id,
                action_intensity=intensity,
                box=box,
                aspect_ratio=aspect
            ))

            current_y += (h + spacing)
            i += 1

        total_height = current_y
        return WebtoonLayout(
            canvas_width=self.W,
            canvas_height=total_height,
            panels=panels_out
        )

if __name__ == "__main__":
    # Test layout algorithm with more diverse mock panels
    mock_panels = [
        {"panel_id": 1, "action_intensity": 1}, # Dialogue -> Will pair with Panel 2
        {"panel_id": 2, "action_intensity": 2}, # Dialogue -> Paired
        {"panel_id": 3, "action_intensity": 3}, # Establishing shot -> Full width square
        {"panel_id": 4, "action_intensity": 2}, # Standalone dialogue
        {"panel_id": 5, "action_intensity": 5}, # Action explosion -> Full height
        {"panel_id": 6, "action_intensity": 1}, # Reaction -> Paired with 7
        {"panel_id": 7, "action_intensity": 1}, # Reaction -> Paired
    ]
    
    agent = LayoutAgent()
    layout = agent.calculate_layout(mock_panels)
    
    print("Layout Canvas Height:", layout.canvas_height)
    for p in layout.panels:
        print(f"Panel {p.panel_id} | Intensity: {p.action_intensity} | Aspect: {p.aspect_ratio} => x:{p.box.x}, y:{p.box.y}, w:{p.box.width}, h:{p.box.height}")
