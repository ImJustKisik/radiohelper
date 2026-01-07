from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Коэффициенты для расчёта дозы
DOSE_COEFFICIENTS = {
    "Голова": {
        ">15 лет": 0.0023,
        "15 лет": 0.00276,
        "10 лет": 0.0046,
        "5 лет": 0.00736,
        "1 год": 0.01173,
        "0-1 год": 0.02185,
    },
    "Туловище": {
        ">15 лет": 0.0081,
        "15 лет": 0.00972,
        "10 лет": 0.01458,
        "5 лет": 0.02106,
        "1 год": 0.03240,
        "0-1 год": 0.06399,
    },
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guide_images/<path:filename>')
def get_guide_image(filename):
    """Отдать изображение из папки guide_images"""
    from flask import send_from_directory
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'guide_images'), filename)

@app.route('/api/improve-complaints', methods=['POST'])
def improve_complaints():
    """Улучшение жалоб через OpenRouter AI"""
    data = request.json
    complaints_text = data.get('text', '').strip()
    api_key = data.get('api_key', '').strip()
    
    if not complaints_text:
        return jsonify({'error': 'Текст жалоб не указан'}), 400
    
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY", "")
    
    if not api_key:
        return jsonify({'error': 'API ключ не указан'}), 400
    
    try:
        improved_text = call_openrouter(complaints_text, api_key)
        return jsonify({'improved_text': improved_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-dose', methods=['POST'])
def calculate_dose():
    """Расчёт эффективной дозы"""
    data = request.json
    
    try:
        dlp = float(data.get('dlp', 0))
        region = data.get('region', 'Голова')
        age = data.get('age', '>15 лет')
        
        if dlp <= 0:
            return jsonify({'error': 'DLP должен быть положительным числом'}), 400
        
        k = DOSE_COEFFICIENTS.get(region, {}).get(age)
        if k is None:
            return jsonify({'error': 'Некорректная область или возраст'}), 400
        
        dose_msv = dlp * k
        dose_text = f"Эффективная доза: {dose_msv:.2f} мЗв (DLP={dlp:.0f}, k={k})"
        
        return jsonify({
            'dose_msv': round(dose_msv, 2),
            'dose_text': dose_text
        })
    except ValueError:
        return jsonify({'error': 'Некорректное значение DLP'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def call_openrouter(complaints_text: str, api_key: str) -> str:
    """Вызов API OpenRouter для улучшения текста"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "radiohelper-web",
        "X-Title": "radiohelper-webapp",
    }
    payload = {
        "model": "google/gemini-3-flash-preview",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты медицинский редактор. Перепиши текст жалоб/анамнеза кратко и профессионально на русском "
                    "в стиле клинических записей, как в примерах: 'На постоянную, средней интенсивности боль...' / "
                    "'Со слов во время ... Хронические заболевания отрицает...'. Требования: 1–3 коротких предложения, "
                    "без списков и кавычек; не добавляй факты, которых нет в исходнике; сохрани отрицания 'отрицает/не отрицает'; "
                    "убери вводные слова про пациента; исправь грамматику и синтаксис, но не выдумывай новые данные."
                ),
            },
            {"role": "user", "content": complaints_text},
        ],
        "temperature": 0.3,
        "max_tokens": 256,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)
    
    if response.status_code == 401:
        raise Exception("Проверьте OPENROUTER_API_KEY")
    
    response.raise_for_status()
    data = response.json()
    
    choices = data.get("choices")
    if not choices:
        raise Exception("Пустой ответ от модели")
    
    content = choices[0].get("message", {}).get("content")
    if not content:
        raise Exception("Модель не вернула текст")
    
    return content.strip()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
