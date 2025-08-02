from flask import Flask, request, send_file
import whisper
import os
import torch
import soundfile as sf
import uuid
import subprocess

app = Flask(__name__)
model = whisper.load_model("tiny")

def text_to_speech(text, output_path):
    subprocess.run(["RHVoice-client", "-s", "Vlad", "-o", output_path], input=text.encode("utf-8"))

def process_command(text):
    if text.lower().startswith("завдання"):
        prompt = text[9:].strip()
        # Замість цього встав свій LLaMA або локальний AI
        # Заглушка:
        response = f"Відповідь на запит: {prompt} — це {eval(prompt) if prompt.replace(' ', '').isdigit() else '42'}"
        return response
    else:
        return "Команду не розпізнано."

@app.route("/ask", methods=["POST"])
def handle_audio():
    audio = request.files["file"]
    temp_input = f"temp_{uuid.uuid4()}.wav"
    temp_output = f"reply_{uuid.uuid4()}.wav"
    audio.save(temp_input)

    try:
        result = model.transcribe(temp_input, language="uk")
        text = result["text"].strip()
        print("Почуто:", text)

        response = process_command(text)
        print("Відповідь:", response)

        text_to_speech(response, temp_output)

        return send_file(temp_output, mimetype="audio/wav")
    except Exception as e:
        return str(e), 500
    finally:
        if os.path.exists(temp_input): os.remove(temp_input)
        if os.path.exists(temp_output): os.remove(temp_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
