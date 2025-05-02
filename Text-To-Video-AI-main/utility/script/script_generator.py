import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "llama3-70b-8192"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
    """You are a video content writer who converts first aid instructions into short, visual-friendly scripts.
Your goal is to turn a step-by-step instruction into a script suitable for an educational short-form video (under 60 seconds).

Each line of the script should describe what's happening visually and match the spoken instruction in tone and pacing.

Output only a JSON object with the key 'script' like below:
{"script": "1. The person gently rinses the burn under cool running water. 2. They pat it dry with a clean towel. 3. A sterile bandage is applied to cover the area. 4. The person elevates the hand to reduce swelling."}
"""
)


    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
