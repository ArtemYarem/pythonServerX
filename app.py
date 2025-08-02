from flask import Flask, request, jsonify
import g4f
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Очікується поле 'text' у JSON"}), 400

        prompt = data['text']
        logging.debug(f"Отримано текст: {prompt}")

        # Запит до g4f
        result = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        logging.debug(f"Відповідь від g4f: {result}")
        return jsonify({"response": result.strip()})

    except Exception as e:
        logging.error(f"Помилка: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
