import os
import copy
from src.backend.agents.narrative_agent import NarrativeAgent
from src.backend.agents.layout_agent import LayoutAgent
from src.worker.comfyui_client import ComfyUIClient
from src.backend.utils.stitch_webtoon import WebtoonStitcher
from src.backend.utils.speech_bubble import SpeechBubbleDrawer
from src.backend.agents.critic_agent import CriticAgent
from dotenv import load_dotenv

load_dotenv()

class WebtoonEngine:
    """
    Core Pipeline Engine that connects all micro-systems sequentially.
    Script -> JSON -> Layout -> AI Generator -> Stitcher -> Speech Bubble -> Output
    """
    def __init__(self, ngrok_url="uncondemned-jonas-distortedly.ngrok-free.dev"):
        print("Initializing Webtoon Pipeline Engine...")
        self.narrative_agent = NarrativeAgent()
        self.layout_agent = LayoutAgent()
        self.ai_client = ComfyUIClient(ngrok_url)
        self.stitcher = WebtoonStitcher()
        self.bubble_drawer = SpeechBubbleDrawer()
        self.critic_agent = CriticAgent()
        print("✅ Pipeline Initialized!")

    def get_closest_multiple_of_64(self, val):
        return max(64, round(val / 64) * 64)

    def run_pipeline(self, script_text: str, project_name: str = "auto_webtoon"):
        print(f"\n🚀 --- STARTING PIPELINE for '{project_name}' ---")
        
        # 1. NARRATIVE
        print("\n[1/5] 📖 Parsing Script with Narrative Agent...")
        storyboard = self.narrative_agent.parse_script(script_text)
        panels_dict_list = [p.model_dump() for p in storyboard.panels]
        print(f"   -> Extracted {len(panels_dict_list)} panels.")

        # 2. LAYOUT
        print("\n[2/5] 📐 Calculating Bounding Boxes with Layout Agent...")
        layout = self.layout_agent.calculate_layout(panels_dict_list)
        print(f"   -> Canvas generated: {layout.canvas_width}x{layout.canvas_height} px.")

        # 3. AI IMAGE GENERATION
        print("\n[3/5] 🤖 Sending Prompts to Colab AI Engine...")
        generated_images = []
        for i, panel in enumerate(panels_dict_list):
            layout_box = layout.panels[i].box
            
            # Clamp width/height for Stable Diffusion
            target_w = self.get_closest_multiple_of_64(layout_box.width)
            target_h = self.get_closest_multiple_of_64(layout_box.height)
            
            # Setup prompt and size
            prompt_str = f"masterpiece, best quality, {panel.get('visual_prompt', '1girl, anime style')}"
            
            workflow = {
                "3": {"class_type": "KSampler", "inputs": {"seed": 1337, "steps": 20, "cfg": 7, "sampler_name": "euler", "scheduler": "normal", "denoise": 1, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
                "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "animagine-xl-3.1.safetensors"}},
                "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": 1, "width": target_w, "height": target_h}},
                "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt_str, "clip": ["4", 1]}},
                "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "lowres, bad anatomy", "clip": ["4", 1]}},
                "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
                "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "webtoon", "images": ["8", 0]}}
            }
                
            print(f"   - Panel {i+1}: Calling Colab ({target_w}x{target_h})...")
            
            max_retries = 2
            attempts = 0
            best_img_path = ""
            
            while attempts < max_retries:
                attempts += 1
                
                # In real execution, call ai_client here:
                # images = self.ai_client.generate_image_from_workflow(workflow, output_dir=f"./output/{project_name}")
                # generated_images.extend(images)
                
                # Mock path
                dummy_path = f"./output/{project_name}/dummy_img_p{i+1}_att{attempts}.png"
                if not os.path.exists(dummy_path):
                    os.makedirs(os.path.dirname(dummy_path), exist_ok=True)
                    from PIL import Image
                    Image.new("RGB", (target_w, target_h), "gray").save(dummy_path)
                
                print(f"     > Critic Agent evaluating attempt {attempts}...")
                eval_result = self.critic_agent.evaluate_image(dummy_path, prompt_str)
                best_img_path = dummy_path
                
                if eval_result.is_accepted:
                    print(f"     ✅ Accepted: {eval_result.reason}")
                    break
                else:
                    print(f"     ❌ Rejected: {eval_result.reason} -> Retrying...")
                    
            generated_images.append(best_img_path)

        # 4. IMAGE STITCHING
        print("\n[4/5] 🧩 Stitching Images into Continuous Webtoon Canvas...")
        stitched_path = f"./output/{project_name}/{project_name}_raw.png"
        self.stitcher.stitch(layout, generated_images, output_path=stitched_path)

        # 5. SMART SPEECH BUBBLE (OPENCV FACE-AWARE)
        print("\n[5/5] 💬 Overlaying Typography (Smart Bubbles avoiding faces)...")
        final_path = f"./output/{project_name}/{project_name}_final.png"
        
        # Draw explicit bubbles avoiding specific paths
        self.bubble_drawer.draw_bubbles(
            image_path=stitched_path,
            layout=layout, 
            narrative_panels=panels_dict_list, 
            output_path=final_path
        )
        
        print("\n🎉 PIPELINE COMPLETE!")
        print(f"Output saved to: {final_path}")
        return final_path

if __name__ == "__main__":
    test_script = "Mia is sitting at the cafe, feeling completely drained.\nMia: I am so tired.\nSuddenly an explosion happens.\nMia: Ahhh!"
    engine = WebtoonEngine()
    engine.run_pipeline(test_script, "test_pipeline")
