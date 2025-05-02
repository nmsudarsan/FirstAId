from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr

from firstaid_brain import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs
from image_generator import generate_images_for_steps

system_prompt = """
You are a certified first aid instructor. Your job is to look at an image and provide calm, clear, and actionable first aid advice. Avoid diagnosis or medical jargon. Focus only on basic, immediate actions a layperson can take. And finally recommend to check with the doctor when it is required.

Here are a few examples:

Example 1:
Image: A person with a scraped knee.
User: I fell and hurt my knee. What should I do?
Assistant: Clean the wound gently with water. Apply an antiseptic if available and cover it with a sterile bandage.

Example 2:
Image: A swollen ankle with redness.
User: I think I twisted my ankle. What should I do?
Assistant: Rest the ankle and avoid putting weight on it. Apply ice for 20 minutes and elevate it above heart level.

Example 3:
Image: A minor kitchen burn on a hand.
User: I burned my hand cooking. What should I do?
Assistant: Hold the burn under cool (not cold) running water for 15 minutes. Cover with a non-stick, sterile bandage and avoid applying creams or ice.

Now, use the same tone and style to respond to the image and user spoken input below.
"""

from image_generator import generate_images_for_steps

def process_inputs(audio_filepath, image_filepath):
    if not audio_filepath or not os.path.exists(audio_filepath):
        return "No audio file detected.", "No response generated.", None, []

    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath_mp3="final.mp3"
    )

    #STEP INSTRUCTION IMAGE GENERATION
    from step_extractor import extract_clean_steps
    stepwise_instructions = extract_clean_steps(doctor_response)
    image_urls = generate_images_for_steps(stepwise_instructions)

    return speech_to_text_output, doctor_response, voice_of_doctor, image_urls

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
    gr.Textbox(label="Speech to Text"),
    gr.Textbox(label="First Aid Instructor's Response"),
    gr.Audio(type="filepath", label="Instructor Voice"),
    gr.Gallery(label="Visual First Aid Instructions", type="filepath", columns=2, height=600),
],
    title="AI First Aid Instructor"
)

iface.launch(debug=True, share=True)