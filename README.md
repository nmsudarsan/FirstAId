
# 🩺 AI First Aid Instructor (Voice + Vision)

# Please go through the AI_FirstAid_Project_Report.pdf file to view input and output, along with the workflow of the project.

This project is an AI-powered **First Aid Instructor** that uses voice input, image analysis, and LLMs to provide actionable, step-by-step medical assistance with **visual illustrations**.

Built using:
- 🔊 **Voice input** via `SpeechRecognition` + Whisper (Groq)
- 🧠 **First aid recommendation** via Groq LLM (`llama3-8b`)
- 🖼️ **Image generation** via Hugging Face FLUX model
- 🗣️ **Text-to-speech** via `gTTS` and `ElevenLabs`
- 🌐 Interactive frontend built with **Gradio**

---

## 🚀 Features

- 🎙️ Record patient voice using microphone
- 🤖 Transcribes voice to text using Whisper model via Groq
- 🧠 Analyzes user speech + image using multimodal LLM (Groq)
- 🖼️ Extracts visual first aid steps and generates step-wise illustrations using Hugging Face
- 🗣️ Responds with spoken instructions using ElevenLabs/gTTS
- 🖼️ Scrollable image gallery for visual aid

---

## 🧱 Tech Stack

| Component            | Library / API                      |
|----------------------|------------------------------------|
| LLM (Text/Image)     | `groq` (LLaMA 3)                    |
| Audio Input          | `speechrecognition`, `pyaudio`     |
| Audio Output         | `gtts`, `elevenlabs`               |
| Audio Handling       | `pydub`, `ffmpeg`                  |
| Image Generation     | Hugging Face FLUX (FLUX.1-dev)     |
| Image Display        | `gradio`                           |
| Prompt Parsing       | `llama3-8b-8192` via Groq API      |

---

## 📦 Setup Instructions

1. **Clone the repo:**
```bash
git clone https://github.com/nmsudarsan/FirstAId.git
cd FirstAId
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your `.env` file:**
Create a `.env` file in the root directory and add:

```
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

5. **Run the app:**
```bash
python gradio_app.py
```

---

## 📁 Directory Structure

```
├── gradio_app.py              # Main Gradio interface
├── voice_of_the_patient.py    # Voice recording + transcription
├── voice_of_the_doctor.py     # TTS voice response
├── firstaid_brain.py          # Multimodal analysis using Groq
├── step_extractor.py          # Extracts + simplifies visual steps
├── image_generator.py         # Uses HF FLUX to generate step images
├── requirements.txt
├── .env (not committed)       # Your API keys
```

---

## 🎨 Sample Output

Please go through AI_FirstAid_Project_Report.pdf file to know more.

---

## 🛡️ Disclaimers

- This is **not a replacement for professional medical advice**.
- Intended for educational and demonstration purposes only.

---

## 🤝 Contributing

Pull requests welcome. For major changes, please open an issue first.

---

## 📜 License

This project is licensed under the MIT License.
