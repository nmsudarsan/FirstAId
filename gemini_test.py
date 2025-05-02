import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "black-forest-labs/FLUX.1-dev"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

# Simple test prompt
prompt = "A flat, minimal illustration of a person applying a bandage to their hand, top-down view, no text"

payload = {
    "inputs": prompt
}

try:
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200 and "image" in response.headers.get("content-type", ""):
        output_path = "hf_flux_test_output.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved to {output_path}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Exception occurred: {e}")
