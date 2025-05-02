# image_generator.py
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "black-forest-labs/FLUX.1-dev"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def generate_images_for_steps(steps: list[str]) -> list[str]:
    image_paths = []

    for i, step in enumerate(steps):
        prompt = f"{step}, flat illustration style, top-down view, minimal medical scene, no text or labels"
        payload = {"inputs": prompt}

        for attempt in range(3):  # Retry up to 3 times
            response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
            
            if response.status_code == 200 and "image" in response.headers.get("content-type", ""):
                image_path = f"step_image_{i+1}.png"
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Image generated: {image_path}")
                image_paths.append(image_path)
                break
            else:
                print(f"⚠️ Attempt {attempt+1} failed for step {i+1}: {response.status_code}")
                time.sleep(3)  # Wait before retrying
        else:
            print(f"❌ Failed to generate image for step {i+1} after 3 attempts.")

    return image_paths
