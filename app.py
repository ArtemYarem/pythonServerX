from flask import Flask, request, jsonify
from PIL import Image
import io
import g4f

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    image = request.files['image']
    image_bytes = image.read()

    # Можеш зберегти тимчасово
    img = Image.open(io.BytesIO(image_bytes))
    img.save("last_upload.jpg")  # опціонально

    # Запит до ШІ
    prompt = "На цьому фото зображено екологічне завдання. Чи виконане воно правильно? Відповідай 'correct' або 'incorrect'."

    # передай картинку, наприклад, у base64, або текстово
    result = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "user", "content": "Фото виконаного завдання надано (уяви його, або опиши)."},
        ]
    )

    response = result.lower()
    if "correct" in response:
        return "correct"
    else:
        return "incorrect"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
