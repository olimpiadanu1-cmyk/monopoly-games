#!/bin/bash

echo "========================================"
echo "   Monopoly Game - Запуск сервера"
echo "========================================"
echo

echo "Запуск сервера..."
python3 simple_server.py &
SERVER_PID=$!

echo
echo "✅ Сервер запущен!"
echo "📖 Откройте в браузере: http://localhost:5000"
echo
echo "Нажмите Ctrl+C для остановки сервера"

# Функция для остановки сервера
cleanup() {
    echo
    echo "Остановка сервера..."
    kill $SERVER_PID 2>/dev/null
    echo "Сервер остановлен."
    exit 0
}

# Обработка сигнала прерывания
trap cleanup SIGINT

# Ожидание
wait

