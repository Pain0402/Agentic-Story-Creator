import json
import urllib.request
import urllib.parse
import os
import websocket
import uuid
import requests

class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        # Automatically strip http:// or https:// if accidentally included
        self.server_address = server_address.replace("https://", "").replace("http://", "").rstrip("/")
        self.client_id = str(uuid.uuid4())
        
    def queue_prompt(self, prompt_workflow):
        p = {"prompt": prompt_workflow, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        protocol = "https" if "ngrok" in self.server_address else "http"
        req = urllib.request.Request(f"{protocol}://{self.server_address}/prompt", data=data)
        req.add_header('ngrok-skip-browser-warning', 'true')
        response = json.loads(urllib.request.urlopen(req).read())
        return response['prompt_id']

    def upload_image(self, image_path, subfolder=""):
        """Uploads an image to ComfyUI server for use in workflows (e.g. IP-Adapter)."""
        protocol = "https" if "ngrok" in self.server_address else "http"
        url = f"{protocol}://{self.server_address}/upload/image"
        
        with open(image_path, "rb") as f:
            files = {"image": (os.path.basename(image_path), f, "image/png")}
            data = {"subfolder": subfolder} if subfolder else {}
            # Need to pass ngrok header if ngrok is used
            headers = {'ngrok-skip-browser-warning': 'true'}
            response = requests.post(url, files=files, data=data, headers=headers)
            
        if response.status_code == 200:
            result = response.json()
            return result.get("name") # Returns the saved filename
        else:
            raise Exception(f"Failed to upload image. Status: {response.status_code}, {response.text}")

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        protocol = "https" if "ngrok" in self.server_address else "http"
        req = urllib.request.Request(f"{protocol}://{self.server_address}/view?{url_values}")
        req.add_header('ngrok-skip-browser-warning', 'true')
        return urllib.request.urlopen(req).read()

    def get_history(self, prompt_id):
        protocol = "https" if "ngrok" in self.server_address else "http"
        req = urllib.request.Request(f"{protocol}://{self.server_address}/history/{prompt_id}")
        req.add_header('ngrok-skip-browser-warning', 'true')
        return json.loads(urllib.request.urlopen(req).read())

    def get_images(self, ws, prompt_id):
        prompt_id_to_history = self.get_history(prompt_id)
        if prompt_id not in prompt_id_to_history:
            return {}
            
        history = prompt_id_to_history[prompt_id]
        output_images = {}
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output
            
        return output_images

    def generate_image_from_workflow(self, workflow_dict, output_dir="./output"):
        """
        Connects via WebSocket to ComfyUI, sends the prompt, waits for execution and downloads images.
        """
        try:
            ws = websocket.WebSocket()
            # If server_address has https:// or http://, strip it for WS
            ws_address = self.server_address.replace("http://", "").replace("https://", "")
            
            # Using standard ws protocol. If Ngrok generates https, we need wss://
            protocol = "wss://" if "ngrok" in self.server_address else "ws://"
            ws.connect(f"{protocol}{ws_address}/ws?clientId={self.client_id}")
            
            prompt_id = self.queue_prompt(workflow_dict)
            print(f"[{prompt_id}] Request queued to ComfyUI. Waiting for execution...")
            
            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        data = message['data']
                        if data['node'] is None and data['prompt_id'] == prompt_id:
                            # Execution is done
                            break
            
            images = self.get_images(ws, prompt_id)
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            saved_paths = []
            for node_id in images:
                for i, image_data in enumerate(images[node_id]):
                    file_path = os.path.join(output_dir, f"panel_{prompt_id}_{node_id}_{i}.png")
                    with open(file_path, "wb") as f:
                        f.write(image_data)
                    saved_paths.append(file_path)
                    print(f"✅ Image saved: {file_path}")
            
            return saved_paths
            
        except Exception as e:
            print(f"❌ Error communicating with ComfyUI: {e}")
            return []

# ----- EXAMPLE USAGE -----
if __name__ == "__main__":
    import copy
    
    # Normally, you load this from a .json file exported by ComfyUI.
    # We are simulating a generic Text2Image layout for Task 8 verification.
    MOCK_WORKFLOW = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": 1337,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            }
        },
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "animagine-xl-3.1.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": 1, "width": 832, "height": 1216}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "masterpiece, best quality, 1girl, short brown hair, tired eyes, drinking coffee in sunlit cafe, anime style", "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "lowres, bad anatomy, bad hands, text, speech bubble, worst quality", "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "webtoon", "images": ["8", 0]}}
    }

    # Example: Replace text dynamically based on Narrative Agent output
    # Change resolution based on Layout Agent Aspect Ratio
    workflow = copy.deepcopy(MOCK_WORKFLOW)
    
    # Normally we would take the layout box width/height and clamp to multiples of 64
    def get_closest_multiple_of_64(val):
        return round(val / 64) * 64
        
    mock_layout_width = 370
    mock_layout_height = 493 
    
    # Adjust resolution in Empty Latent Image (Node "5")
    workflow["5"]["inputs"]["width"] = get_closest_multiple_of_64(mock_layout_width)
    workflow["5"]["inputs"]["height"] = get_closest_multiple_of_64(mock_layout_height)
    
    # Change address to your Ngrok URL when testing against Colab
    client = ComfyUIClient("uncondemned-jonas-distortedly.ngrok-free.dev") 
    print(f"Testing ComfyUI Client with URL: {client.server_address}")
    print(f"-> Generating image with resolution {workflow['5']['inputs']['width']}x{workflow['5']['inputs']['height']}...")
    # Uncomment to actually run against Colab
    # images = client.generate_image_from_workflow(workflow, output_dir="./output") 
    # print(f"Done! Generated {len(images)} images.")
