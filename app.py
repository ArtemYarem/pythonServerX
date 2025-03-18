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

    if ind == 1:
        param1 = data.get('paramr1')
        param2 = data.get('paramr2')
        param3 = data.get('paramr3')
        param4 = data.get('paramr4')
        param5 = data.get('paramr5')
        param6 = data.get('paramr6')
        param7 = data.get('paramr7')
        param8 = data.get('paramr8')
        param9 = data.get('paramr9')
        param10 = data.get('paramr10')
        param11 = data.get('paramr11')
        param12 = data.get('paramr12')
        param13 = data.get('paramr13')
        param14 = data.get('paramr14')
        param15 = data.get('paramr15')
        param16 = data.get('paramr16')
        param17 = data.get('paramr17')
        param18 = data.get('paramr18')
        param19 = data.get('paramr19')
        param20 = data.get('paramr20')
        param21 = data.get('paramr21')
        param22 = data.get('paramr22')
        param23 = data.get('paramr23')
        param24 = data.get('paramr24')
        param25 = data.get('paramr25')
        param26 = data.get('paramr26')
        param27 = data.get('paramr27')
        param28 = data.get('paramr28')
        param29 = data.get('paramr29')
        param30 = data.get('paramr30')
    
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user",
                       "content": f"Дуже коротко опиши які витрати можна в бізнесі скоротити (але в кінці напиши щось типу вибір за вами)   RENT: {param1}, UTILITIES: {param2}, SALARIES: {param3}, TAXES: {param4}, OFFICE SUPPLIES: {param5}, MARKETING: {param6}, MATERIALS: {param7}, LOGISTICS: {param8}, INSURANCE: {param9}, EQUIPMENT: {param10}, MAINTENANCE: {param11}, WEBSITE COSTS: {param12}, SOFTWARE: {param13}, BANK FEES: {param14}, LICENSES: {param15}, CONSULTING: {param16}, TRAINING: {param17}, TRAVEL: {param18}, CLIENT MEETINGS: {param19}, SECURITY: {param20}, RENT: {param21}, R&D: {param22}, CERTIFICATION: {param23}, WASTE DISPOSAL: {param24}, PACKAGING: {param25}, DISCOUNTS: {param26}, PARTNERSHIPS: {param27}, PHONE & INTERNET: {param28}, CHARITY: {param29}, OTHERS: {param30} англійською та всі літери з великої"}],
            web_search=False
        )

    elif ind == 2:
        param31 = data.get('paramrx')
        param32 = data.get('paramry')

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user",
                       "content": f"Напиши привіт"}],
            web_search=False
        )

    else:
        return jsonify({"description": "Невідомий індекс"})

    description = response.choices[0].message.content
    return jsonify({"description": description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
