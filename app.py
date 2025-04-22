from flask import Flask, request, jsonify
from PIL import Image
import io
import g4f
import base64
import logging

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/get_description', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            logging.error("Зображення не знайдено в запиті.")
            return jsonify({"error": "Зображення не знайдено в запиті."}), 400
        
        image = request.files['image']
        image_bytes = image.read()

        # Відкриваємо зображення
        img = Image.open(io.BytesIO(image_bytes))

        if img.mode == 'RGBA':
            img = img.convert('RGB')
            logging.debug("Зображення конвертовано з RGBA в RGB.")

        img.save("last_upload.jpg", 'JPEG')
        logging.debug("Зображення успішно отримано та збережено.")

        # Підготовка запиту
        prompt = "Чи робиться на цьому фото щось екологічне? Відповідай 'correct' якщо так або 'incorrect' якщо ні (одним словом)."

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        if len(image_base64) > 2_000_000:
            logging.warning("base64 зображення обрізано через розмір.")
            image_base64 = image_base64[:2_000_000]

        try:
            result = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": "Фото виконаного завдання надано (уяви його, або опиши)."},
                    {"role": "system", "content": f"Фото в base64: {image_base64}"}
                ]
            )
            response = result.strip().lower() if result else "incorrect"
        except Exception as e:
            logging.error(f"g4f помилка: {str(e)}")
            response = "incorrect"

        logging.info(f"Відповідь AI: {response}")
        return response

    except Exception as e:
        logging.error(f"Помилка: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
