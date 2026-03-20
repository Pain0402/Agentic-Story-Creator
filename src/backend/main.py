from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
from src.backend.agents.narrative_agent import NarrativeAgent
from src.backend.agents.layout_agent import LayoutAgent
from src.backend.engine import WebtoonEngine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
import os
import uuid
from dotenv import load_dotenv
import sys
import shutil
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

app = FastAPI(title="AnimeAI Webtoon Orchestrator", version="1.0")

# Setup CORS for Frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the output directory containing generated Webtoons statically
os.makedirs("output", exist_ok=True)
app.mount("/static", StaticFiles(directory="output"), name="static")

class ScriptRequest(BaseModel):
    script_text: str

# Validate API Key on startup
if not os.getenv("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY is not set in environment variables.")

# Instantiate agent
try:
    narrative_agent = NarrativeAgent()
    layout_agent = LayoutAgent()
    engine = WebtoonEngine()
except Exception as e:
    print(f"Error initializing Agents or Engine: {e}")
    narrative_agent = None
    layout_agent = None
    engine = None


@app.post("/api/v1/parse-script")
def parse_script(request: ScriptRequest):
    """
    Parses a raw text script into a structured storyboard JSON containing characters, 
    panels, visual prompts, and dialogue.
    """
    if narrative_agent is None:
        raise HTTPException(status_code=500, detail="Narrative Agent is not initialized.")
    if not request.script_text.strip():
        raise HTTPException(status_code=400, detail="Script text cannot be empty.")
        
    try:
        # The agent returns a StoryboardSchema (Pydantic model)
        result = narrative_agent.parse_script(request.script_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/generate-layout")
def generate_layout(request: ScriptRequest):
    """
    Parses a raw text script into a structured storyboard, and then calculates the 
    Webtoon layout canvas with precise bounding boxes for each panel.
    """
    if narrative_agent is None or layout_agent is None:
        raise HTTPException(status_code=500, detail="Agents are not initialized.")
    if not request.script_text.strip():
        raise HTTPException(status_code=400, detail="Script text cannot be empty.")
        
    try:
        # 1. Parse Script to generate Narrative Panels
        narrative_result = narrative_agent.parse_script(request.script_text)
        
        # 2. Extract panels as a list of dicts to feed the Layout Agent
        panels_dict_list = [p.model_dump() for p in narrative_result.panels]
        
        # 3. Calculate Layout Coordinates
        layout_result = layout_agent.calculate_layout(panels_dict_list)
        
        return {
            "narrative": narrative_result.model_dump(),
            "layout": layout_result.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v3/generate-webtoon")
async def generate_webtoon(
    script_text: str = Form(...),
    reference_image: UploadFile = File(None)
):
    """
    The ultimate End-to-End endpoint.
    Runs the full Narrative -> Layout -> CV -> Colab AI -> Stitching -> Typography pipeline.
    """
    if engine is None:
        raise HTTPException(status_code=500, detail="Webtoon Engine is not initialized.")
    if not script_text.strip():
        raise HTTPException(status_code=400, detail="Script text cannot be empty.")
        
    try:
        # Create a unique project ID for this generation request
        project_id = f"webtoon_{uuid.uuid4().hex[:8]}"
        
        # Save uploaded reference image to a temporary file
        ref_image_path = None
        if reference_image is not None:
            temp_dir = tempfile.mkdtemp()
            ref_image_path = os.path.join(temp_dir, reference_image.filename)
            with open(ref_image_path, "wb") as buffer:
                shutil.copyfileobj(reference_image.file, buffer)
        
        # Run the massive background pipeline 
        final_image_path = engine.run_pipeline(script_text, project_name=project_id, reference_image_path=ref_image_path)
        
        # Clean up temp file
        if ref_image_path and os.path.exists(ref_image_path):
            try:
                os.remove(ref_image_path)
                os.rmdir(os.path.dirname(ref_image_path))
            except Exception as e:
                print(f"Cleanup error: {e}")
        
        # Convert local path to a URL accessible by Frontend: ./output/project/file.png -> /static/project/file.png
        url_path = final_image_path.replace("./output\\", "/static/").replace("./output/", "/static/")
        
        return {
            "status": "success",
            "project_id": project_id,
            "final_webtoon_url": url_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # When running directly with `python src/backend/main.py`
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)
