#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Папка для хранения данных (можно переопределить через переменную окружения DATA_DIR)
DATA_DIR = os.environ.get('DATA_DIR', 'data')

# Файлы для хранения данных
DATA_FILES = {
    'users': 'users.json',
    'applications': 'applications.json',
    'purchase_requests': 'purchase_requests.json',
    'task_submissions': 'task_submissions.json',
    'reward_history': 'reward_history.json',
    'leaderboard': 'leaderboard.json',
    'cell_tasks': 'cell_tasks.json',
    'game_states': 'game_states.json',
    'shop_items': 'shop_items.json',
    'shopping_carts': 'shopping_carts.json'
}

# Папка для загрузок скриншотов
UPLOADS_DIR = os.path.join('.', 'uploads')
TASK_SCREENSHOTS_DIR = os.path.join(UPLOADS_DIR, 'task_submissions')
os.makedirs(TASK_SCREENSHOTS_DIR, exist_ok=True)

def load_data(data_type):
    """Загрузить данные из JSON файла"""
    if data_type not in DATA_FILES:
        return None
        
    file_path = os.path.join(DATA_DIR, DATA_FILES[data_type])
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Возвращаем пустые данные по умолчанию
            if data_type in ['users', 'applications', 'purchase_requests', 'task_submissions', 'reward_history', 'leaderboard', 'cell_tasks', 'shop_items']:
                return []
            else:  # game_states, shopping_carts
                return {}
    except Exception as e:
        print(f"Ошибка загрузки {data_type}: {e}")
        return [] if data_type != 'game_states' and data_type != 'shopping_carts' else {}

def save_data(data_type, data):
    """Сохранить данные в JSON файл"""
    if data_type not in DATA_FILES:
        return False

# Загрузка скриншотов заданий
@app.route('/api/upload-screenshots', methods=['POST'])
def upload_screenshots():
    try:
        # Идентификатор отправки, чтобы группировать файлы
        submission_id = request.form.get('submissionId') or str(int(os.path.getmtime(__file__)))
        target_dir = os.path.join(TASK_SCREENSHOTS_DIR, submission_id)
        os.makedirs(target_dir, exist_ok=True)

        files = request.files.getlist('files')
        saved = []
        for f in files:
            if not f:
                continue
            filename = secure_filename(f.filename)
            # Добавляем уникальный префикс чтобы избежать коллизий
            unique_name = f"{int(os.path.getmtime(__file__))}_{filename}"
            save_path = os.path.join(target_dir, unique_name)
            f.save(save_path)
            public_url = f"/uploads/task_submissions/{submission_id}/{unique_name}"
            saved.append({
                'url': public_url,
                'fileName': filename
            })

        return jsonify({'success': True, 'files': saved})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
        
    file_path = os.path.join(DATA_DIR, DATA_FILES[data_type])
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено: {data_type} -> {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения {data_type}: {e}")
        return False

# API для получения данных
@app.route('/api/data/<data_type>', methods=['GET'])
def get_data(data_type):
    """Получить данные определенного типа"""
    try:
        data = load_data(data_type)
        if data is not None:
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'error': 'Неизвестный тип данных'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API для сохранения данных
@app.route('/api/data/<data_type>', methods=['POST'])
def save_data_endpoint(data_type):
    """Сохранить данные определенного типа"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'success': False, 'error': 'Нет данных'}), 400
        
        success = save_data(data_type, data)
        if success:
            return jsonify({'success': True, 'message': f'Данные {data_type} сохранены'})
        else:
            return jsonify({'success': False, 'error': 'Ошибка сохранения'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API для получения всех данных сразу
@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    """Получить все данные игры"""
    try:
        all_data = {}
        for data_type in DATA_FILES.keys():
            all_data[data_type] = load_data(data_type)
        
        return jsonify({'success': True, 'data': all_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Проверка статуса
@app.route('/api/status', methods=['GET'])
def get_status():
    """Получить статус сервера"""
    return jsonify({'success': True, 'message': 'Сервер работает'})

# Обслуживание главной страницы
@app.route('/')
def serve_index():
    """Обслуживание главной страницы"""
    try:
        return send_file('index.html')
    except Exception as e:
        return f"Error loading index.html: {e}", 500

# Обслуживание статических файлов
@app.route('/<path:filename>')
def serve_static(filename):
    """Обслуживание статических файлов"""
    # Проверяем, что это не API маршрут
    if filename.startswith('api/'):
        return jsonify({'error': 'API route not found'}), 404
    
    # Отдача загруженных скриншотов
    if filename.startswith('uploads/'):
        try:
            return send_from_directory('.', filename)
        except Exception as e:
            return f"Error loading {filename}: {e}", 404

    # Обслуживаем статические файлы
    if filename.endswith(('.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
        try:
            return send_from_directory('.', filename)
        except Exception as e:
            return f"Error loading {filename}: {e}", 404
    else:
        # Для всех остальных файлов возвращаем index.html (SPA)
        try:
            return send_file('index.html')
        except Exception as e:
            return f"Error loading index.html: {e}", 500

if __name__ == '__main__':
    print("Запуск сервера Monopoly Game...")
    print("Папка для данных:", DATA_DIR)
    print("Файлы данных:", list(DATA_FILES.keys()))
    print("Сервер доступен по адресу: http://localhost:5000")
    print("Игра: http://localhost:5000")
    print("API документация: http://localhost:5000/api/status")
    
    # Получаем порт из переменной окружения (для Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

