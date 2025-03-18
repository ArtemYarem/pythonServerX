from flask import Flask, request, jsonify
from g4f.client import Client
import json
from flask_cors import CORS
import os

# Задаємо шлях до файлу на робочому столі
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "playerData.txt")

# Перевіряємо, чи існує файл перед його відкриттям
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
else:
    raise FileNotFoundError(f"Файл за шляхом {file_path} не знайдений!")

# Отримуємо значення ind
ind = data.get("ind", 0)  # Якщо ключа немає, буде 0

app = Flask(__name__)
CORS(app)

@app.route('/get_description', methods=['POST'])
def get_description():
    data = request.json
    client = Client()

    # Перевірка чи отримано індекс
    print(f"Отриманий індекс: {data.get('ind')}")

    # Перевіряємо, чи індекс вірний
    if 'ind' not in data:
        return jsonify({"description": "Індекс не надано!"})

    ind_from_request = data['ind']  # Отримуємо індекс з запиту

    if ind_from_request == 1:
        # Ваш код для індексу 1
        param1 = data.get('paramr1')
        # Продовжуємо з іншими параметрами
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Ваш запит для індексу 1"}],
            web_search=False
        )

    elif ind_from_request == 2:
        # Ваш код для індексу 2
        param31 = data.get('paramrx')
        param32 = data.get('paramry')

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Привіт"}],
            web_search=False
        )

    else:
        return jsonify({"description": "Невідомий індекс"})

    description = response.choices[0].message.content
    return jsonify({"description": description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
