from typing import List, Optional
from pydantic import BaseModel, Field

class CharacterDef(BaseModel):
    name: str = Field(description="Name of the character")
    tags: str = Field(description="Visual tags describing the character's appearance (e.g., 'boy, black messy hair, school_uniform')")

class DialogueBlock(BaseModel):
    speaker: str = Field(description="Name of the character speaking")
    text: str = Field(description="The actual dialogue text spoken by the character within this panel")

class PanelDef(BaseModel):
    panel_id: int = Field(description="Sequential ID of the panel (e.g., 1, 2, 3...)")
    action_intensity: int = Field(
        description="Rating of action intensity from 1 (calm, dialogue heavy) to 5 (explosive, action, climax)",
        ge=1, le=5
    )
    visual_prompt: str = Field(description="Highly descriptive visual cue for AI generation (Danbooru styling) including scene, camera angle, character action")
    dialogue: List[DialogueBlock] = Field(description="List of dialogues happening in this panel", default_factory=list)

class StoryboardSchema(BaseModel):
    total_panels: int = Field(description="Total number of panels in this generated storyboard sequence")
    characters: List[CharacterDef] = Field(description="List of characters appearing or mentioned in the script")
    panels: List[PanelDef] = Field(description="Ordered list of comic panels to be generated")
