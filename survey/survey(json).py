from flask import Flask, render_template, request, url_for
import os
from datetime import datetime
import json

app = Flask(__name__)

# Шлях до папки для збереження відповідей
SURVEY_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses')
os.makedirs(SURVEY_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Отримання даних з форми
        name = request.form.get('name')
        email = request.form.get('email')
        multiple_choices = request.form.getlist('multiple[]')  # Отримання всіх вибраних чекбоксів
        japan_answer = request.form.get('japan')
        china_answer = request.form.get('china')
        country_answer = request.form.get('country')

        # Формування даних для збереження
        data = {
            'name': name,
            'email': email,
            'answers': {
                'interests': multiple_choices,
                'japan': japan_answer,
                'china': china_answer,
                'country': country_answer
            },
            'submitted_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Формування імені файлу з датою та часом
        filename = datetime.now().strftime("response_%Y%m%d_%H%M%S.json")
        filepath = os.path.join(SURVEY_FOLDER, filename)

        # Збереження даних у форматі JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Відображення підтвердження з датою та часом
        submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Thank you for your response! Submitted on {submit_time}."

    return render_template('survey.html', submitted=False)

if __name__ == '__main__':
    app.run(debug=True)
