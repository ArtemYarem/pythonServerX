from flask import Flask, request, jsonify
from PIL import Image
import io
import g4f
import base64

app = Flask(__name__)

@app.route('/get_description', methods=['POST'])
def analyze_image():
    try:
        # Отримуємо зображення з запиту
        image = request.files['image']
        image_bytes = image.read()

        # Можеш зберегти тимчасово для перевірки
        img = Image.open(io.BytesIO(image_bytes))
        img.save("last_upload.jpg")  # зберігає зображення на диск (опціонально)

        # Створюємо запит до ШІ
        prompt = "На цьому фото зображено екологічне завдання. Чи виконане воно правильно? Відповідай 'correct' або 'incorrect'."

        # Перетворюємо зображення у base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Виконуємо запит до моделі g4f
        result = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Фото виконаного завдання надано (уяви його, або опиши)."},
                {"role": "system", "content": f"Фото в base64: {image_base64}"}
            ]
        )

        # Отримуємо відповідь від моделі
        response = result.lower()
        if "correct" in response:
            return "correct"
        else:
            return "incorrect"

    except Exception as e:
        # Логування помилки
        print(f"Помилка: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
