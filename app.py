from flask import Flask, request, jsonify
from PIL import Image
import base64, io, uuid, threading, time, os, json
import g4f

app = Flask(__name__)
os.makedirs("tasks", exist_ok=True)

# --- Фоновий обробник ---
def process_task(task_id, image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        prompt = "Чи робиться на цьому фото щось екологічне? Відповідай 'correct' або 'incorrect'."

        result = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Фото виконаного завдання надано."},
                {"role": "system", "content": f"Фото в base64: {image_base64}"}
            ]
        )

        response = result.lower().strip()

        with open(f"tasks/task_{task_id}.json", "w") as f:
            json.dump({"status": "done", "result": response}, f)

    except Exception as e:
        with open(f"tasks/task_{task_id}.json", "w") as f:
            json.dump({"status": "error", "error": str(e)}, f)

# --- Єдиний /get_description ---

@app.route('/get_description', methods=['POST', 'GET'])
def get_description():
    if request.method == 'POST':
        # Надходить зображення
        if 'image' not in request.files:
            return jsonify({"error": "Image is required"}), 400

        image = request.files['image'].read()
        task_id = str(uuid.uuid4())

        # Зберегти стан
        with open(f"tasks/task_{task_id}.json", "w") as f:
            json.dump({"status": "processing"}, f)

        # Запустити у фоні
        threading.Thread(target=process_task, args=(task_id, image)).start()

        return jsonify({"task_id": task_id}), 202

    elif request.method == 'GET':
        # Запит статусу
        task_id = request.args.get("task_id")
        if not task_id:
            return jsonify({"error": "task_id is required"}), 400

        task_path = f"tasks/task_{task_id}.json"
        if not os.path.exists(task_path):
            return jsonify({"error": "task not found"}), 404

        with open(task_path, "r") as f:
            data = json.load(f)
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
