import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

# System prompt for simplifying steps
visual_batch_prompt = """
You are a visual prompt converter for a medical AI illustration tool.

You will receive a JSON list of first aid steps.

Your job is to:
1. Review each step.
2. If the step can be illustrated visually, rewrite it as a short, simple prompt for image generation.
3. If the step is not visual or is too abstract, ignore it.

Output:
- Return only the simplified visual prompts as a valid JSON list of strings
- Do NOT return skipped steps
- Do NOT add explanation, markdown, or text outside the list
"""

def extract_clean_steps(raw_response: str) -> list[str]:
    # Step 1: Extract raw first aid steps
    extract_prompt = """
You are a medical instruction parser. 
Your job is to extract only step-by-step first aid instructions from the given response.

Format strictly as a valid JSON list of strings like:
["Step 1: Do this.", "Step 2: Do that."]

Do NOT return markdown, explanation, or anything else.
"""

    messages = [
        {"role": "system", "content": extract_prompt},
        {"role": "user", "content": raw_response}
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.2,
        )
        content = response.choices[0].message.content
        print("\n🧠 LLM RAW OUTPUT (extracted steps):\n", content)

        raw_steps = json.loads(content)

    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Falling back to line-splitting.")
        raw_steps = [line.strip() for line in content.strip().splitlines() if line.strip()]
    except Exception as e:
        print(f"❌ Error extracting steps: {e}")
        return []

    # Step 2: Simplify steps for image generation
    simplify_messages = [
        {"role": "system", "content": visual_batch_prompt},
        {"role": "user", "content": json.dumps(raw_steps)}
    ]

    try:
        simplify_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=simplify_messages,
            temperature=0.2,
        )
        simplified_output = simplify_response.choices[0].message.content
        print("\n🎯 Simplified Visual Prompts:\n", simplified_output)

        simplified_steps = json.loads(simplified_output)
        return simplified_steps

    except Exception as e:
        print(f"❌ Error simplifying visual steps: {e}")
        return []
