from typing import List, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x: int = Field(description="X coordinate of the top-left corner")
    y: int = Field(description="Y coordinate of the top-left corner")
    width: int = Field(description="Width of the panel in pixels")
    height: int = Field(description="Height of the panel in pixels")

class LayoutPanel(BaseModel):
    panel_id: int = Field(description="ID matching the Narrative Panel")
    action_intensity: int = Field(description="Action intensity from 1 to 5")
    box: BoundingBox = Field(description="Coordinates and sizes of the panel on the canvas")
    aspect_ratio: str = Field(description="Textual representation of ratio (e.g. 16:9, 1:1, 9:16)")

class WebtoonLayout(BaseModel):
    canvas_width: int = Field(default=800, description="Standard Webtoon rolling canvas width is usually 800px")
    canvas_height: int = Field(description="Total height calculates down to the end of all panels")
    panels: List[LayoutPanel] = Field(description="Computed sequence of all layout frames")
