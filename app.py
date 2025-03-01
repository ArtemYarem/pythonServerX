from flask import Flask, request, jsonify
from g4f.client import Client
import os
import schedule
import time
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


read_data = None


@app.route('/get_description', methods=['POST'])
def get_description():
    data = request.json

    param1 = data.get('param1')
    param2 = data.get('param2')
    param3 = data.get('param3')
    param4 = data.get('param4')
    param5 = data.get('param5')
    param6 = data.get('param6')
    param7 = data.get('param7')
    param8 = data.get('param8')

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user",
                   "content": f"Одним словом опиши комп'ютер з характеристиками: {param1}, {param2}, {param3}, {param4}, {param5}, {param6}, {param7}, {param8}  англійською всі літери з великої типу: GOOD або BAD, MEDIUM і тд"}],
        web_search=False
    )

    description = response.choices[0].message.content
    return jsonify({"description": description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
