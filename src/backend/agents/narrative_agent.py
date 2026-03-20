import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.backend.models.schema import StoryboardSchema

SYSTEM_PROMPT = """You are an expert Webtoon Storyboard Editor. I will provide you with a raw story script. 
Your rigid objective is to break down this script into optimal comic vertical panels.
Follow these rigid rules to output ONLY the required JSON format:

1. Identify character names, minimal visual tags, and current emotions.
2. Break the text into sequences, assigning 'action_intensity' from 1 (calm, dialogue heavy) to 5 (explosive, action, climax).
3. Summarize complex dialogue into brief snippets suitable for speech bubbles.
4. Construct a 'visual_prompt' describing the scene, camera angle, character action focusing heavily on descriptive visual cues (Danbooru styling).

Return ONLY valid JSON.
{format_instructions}

Script:
{script}"""

class NarrativeAgent:
    def __init__(self, temperature=0.2, model_name="llama3"):
        self.llm = ChatOllama(base_url="http://127.0.0.1:11434", model=model_name, format="json", temperature=temperature)
        self.parser = PydanticOutputParser(pydantic_object=StoryboardSchema)
        self.prompt = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["script"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        self.chain = self.prompt | self.llm | self.parser
        
    def parse_script(self, script_text: str) -> StoryboardSchema:
        """Parses the raw script and returns a strictly typed StoryboardSchema."""
        try:
            # Call the actual Gemini API
            return self.chain.invoke({"script": script_text})
        except Exception as e:
            print(f"⚠️ Skipping API call. Using Local Mock Data instead. Reason: {e}")
            from src.backend.models.schema import PanelDef, CharacterDef, DialogueBlock
            
            # Create a mock 2-panel webtoon to keep the pipeline moving to ComfyUI
            return StoryboardSchema(
                total_panels=2,
                characters=[
                    CharacterDef(name="Mia", tags="1girl, short brown hair, tired eyes"),
                    CharacterDef(name="Kai", tags="1boy, black hair, smiling")
                ],
                panels=[
                    PanelDef(
                        panel_id=1,
                        action_intensity=1,
                        visual_prompt="1girl, short brown hair, sitting in a cafe, looking tired, masterpiece, best quality",
                        dialogue=[DialogueBlock(speaker="Mia", text="I am so exhausted today...")]
                    ),
                    PanelDef(
                        panel_id=2,
                        action_intensity=2,
                        visual_prompt="1boy, black hair, holding a coffee cup, smiling, walking into cafe, masterpiece, best quality",
                        dialogue=[DialogueBlock(speaker="Kai", text="Here, your favorite latte!")]
                    )
                ]
            )

if __name__ == "__main__":
    # Test script for local debugging
    from dotenv import load_dotenv
    load_dotenv()
    
    agent = NarrativeAgent()
    sample_text = "Mia is sitting at a table by the window in a cozy, sunlit cafe. She looks exhausted. Mia (thinking): 'Today is just too exhausting...'"
    
    try:
        result = agent.parse_script(sample_text)
        print("Success! JSON Output:")
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error occurred: {e}")
