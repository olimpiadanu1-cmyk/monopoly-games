#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import json
import os
import urllib.parse
from urllib.parse import urlparse, parse_qs

# Папка для хранения данных
DATA_DIR = 'data'

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
        
    file_path = os.path.join(DATA_DIR, DATA_FILES[data_type])
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено: {data_type} -> {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения {data_type}: {e}")
        return False

class MonopolyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)
        
        # API маршруты
        if parsed_path.path.startswith('/api/'):
            self.handle_api_get(parsed_path)
        else:
            # Статические файлы
            super().do_GET()
    
    def do_POST(self):
        """Обработка POST запросов"""
        parsed_path = urlparse(self.path)
        
        # API маршруты
        if parsed_path.path.startswith('/api/'):
            self.handle_api_post(parsed_path)
        else:
            self.send_error(404, "Not Found")
    
    def handle_api_get(self, parsed_path):
        """Обработка API GET запросов"""
        path = parsed_path.path
        
        if path == '/api/status':
            self.send_json_response({'success': True, 'message': 'Сервер работает'})
        elif path.startswith('/api/data/'):
            data_type = path.split('/')[-1]
            data = load_data(data_type)
            if data is not None:
                self.send_json_response({'success': True, 'data': data})
            else:
                self.send_json_response({'success': False, 'error': 'Неизвестный тип данных'}, 400)
        elif path == '/api/all-data':
            all_data = {}
            for data_type in DATA_FILES.keys():
                all_data[data_type] = load_data(data_type)
            self.send_json_response({'success': True, 'data': all_data})
        else:
            self.send_json_response({'error': 'API route not found'}, 404)
    
    def handle_api_post(self, parsed_path):
        """Обработка API POST запросов"""
        path = parsed_path.path
        
        if path.startswith('/api/data/'):
            data_type = path.split('/')[-1]
            
            # Читаем данные из тела запроса
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                success = save_data(data_type, data)
                if success:
                    self.send_json_response({'success': True, 'message': f'Данные {data_type} сохранены'})
                else:
                    self.send_json_response({'success': False, 'error': 'Ошибка сохранения'}, 500)
            except Exception as e:
                self.send_json_response({'success': False, 'error': str(e)}, 500)
        else:
            self.send_json_response({'error': 'API route not found'}, 404)
    
    def send_json_response(self, data, status_code=200):
        """Отправка JSON ответа"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Обработка OPTIONS запросов для CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    PORT = 5000
    
    print("Запуск сервера Monopoly Game...")
    print("Папка для данных:", DATA_DIR)
    print("Файлы данных:", list(DATA_FILES.keys()))
    print("Сервер доступен по адресу: http://localhost:5000")
    print("Игра: http://localhost:5000")
    print("API документация: http://localhost:5000/api/status")
    
    with socketserver.TCPServer(("", PORT), MonopolyHTTPRequestHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()

