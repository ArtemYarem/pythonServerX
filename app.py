from flask import Flask, request, jsonify
from PIL import Image
import io
import g4f
import base64
import logging
import signal

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

# Тайм-аут в секундах
TIMEOUT = 999  # Збільшіть це значення для довших запитів

# Функція для обробки тайм-ауту
def timeout_handler(signum, frame):
    raise TimeoutError("Запит перевищує максимальний ліміт часу")

signal.signal(signal.SIGALRM, timeout_handler)

app = Flask(__name__)

@app.route('/get_description', methods=['POST'])
def analyze_image():
    try:
        # Встановлюємо тайм-аут на час виконання запиту
        signal.alarm(TIMEOUT)  # Встановлює тайм-аут

        # Перевірка наявності зображення
        if 'image' not in request.files:
            logging.error("Зображення не знайдено в запиті.")
            return jsonify({"error": "Зображення не знайдено в запиті."}), 400
        
        image = request.files['image']
        image_bytes = image.read()

        # Перевірка валідності зображення
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()  # Перевірка валідності
            img = Image.open(io.BytesIO(image_bytes))  # Повторне відкриття після verify()
        except Exception as img_error:
            logging.error(f"Помилка при обробці зображення: {img_error}")
            return jsonify({"error": "Невалідне зображення"}), 400

        # Якщо RGBA — конвертувати в RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            logging.debug("Зображення конвертовано з RGBA в RGB.")

        # Збереження для перевірки
        img.save("last_upload.jpg", 'JPEG')

        logging.debug("Зображення успішно збережено та підготовлено.")

        # Запит до ШІ
        prompt = "Чи робиться на цьому фото щось екологічне? Відповідай 'correct' якщо так або 'incorrect' якщо ні (лише 1 словом)."

        # Перетворення в base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        logging.debug("Перетворення зображення в base64 завершено.")

        # Виклик g4f
        try:
            logging.debug("Запит до g4f розпочато.")
            result = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": "Фото виконаного завдання надано (уяви його, або опиши)."},
                    {"role": "system", "content": f"Фото в base64: {image_base64}"}
                ],
                timeout=TIMEOUT  # Встановлення тайм-ауту для запиту до g4f
            )
            logging.debug(f"Відповідь від g4f: {result}")

            response = result.lower().strip()
        except Exception as gpt_error:
            logging.error(f"Помилка у g4f: {gpt_error}")
            return jsonify({"error": f"g4f error: {str(gpt_error)}"}), 500

        # Обробка відповіді
        if response == "correct":
            logging.info("Завдання виконано правильно.")
            return "correct"
        else:
            logging.info("Завдання виконано неправильно.")
            return "incorrect"

    except TimeoutError as e:
        logging.error("Запит перевищив максимальний час.")
        return jsonify({"error": "Запит перевищив максимальний час."}), 504
    except Exception as e:
        logging.error(f"Загальна помилка: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        signal.alarm(0)  # Скидає сигнал тайм-ауту

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
