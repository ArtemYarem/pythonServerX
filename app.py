from flask import Flask, request, jsonify
from g4f.client import Client
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_description', methods=['POST'])
def get_description():
    data = request.json
    ind = data.get("ind", 0)  # Отримуємо значення ind з запиту

    client = Client()

    param1 = data.get('paramrr1')
    param2 = data.get('paramrr2')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user",
                   "content": f"Дуже дуже дуже коротко (приблизно 5 - 10 слів) опиши стан людини якщо уважність людини(від 0 до 1): {param1}, а стресс, засмученість(від 0 до 1): {param2}, напиши англійською та всі літери з великої"}],
        web_search=False
    )

    description = response.choices[0].message.content
    return jsonify({"description": description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
