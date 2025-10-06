# 🚀 API Architecture - Monopoly Game

## 📋 Новая архитектура с API сервером

### 🔄 **Как это работает:**

1. **Загрузка страницы** → JavaScript загружает данные с Python API сервера
2. **Действия пользователя** → Данные сохраняются на сервер через API
3. **localStorage** → Используется только как backup и для кеширования

### 🏗️ **Компоненты системы:**

#### 1. **API Сервер** (`api_server.py`)
- **Порт**: 5000
- **Функции**:
  - `GET /api/status` - проверка статуса
  - `GET /api/data/{type}` - загрузка данных определенного типа
  - `POST /api/data/{type}` - сохранение данных
  - `GET /api/all-data` - загрузка всех данных сразу

#### 2. **API Клиент** (`api_client.js`)
- **Класс**: `MonopolyAPI`
- **Функции**:
  - `checkStatus()` - проверка доступности сервера
  - `loadData(type)` - загрузка данных
  - `saveData(type, data)` - сохранение данных
  - `loadAllData()` - загрузка всех данных
  - Кеширование с таймаутом 5 секунд

#### 3. **Обновленный script.js**
- **Загрузка**: `loadAllDataFromServer()` - загружает все данные при старте
- **Сохранение**: `saveToServer()` - сохраняет данные на сервер
- **Fallback**: `loadFromLocalStorage()` - если сервер недоступен

### 📊 **Типы данных:**

| Тип | Описание | Файл |
|-----|----------|------|
| `users` | Пользователи | `data/users.json` |
| `applications` | Заявки на регистрацию | `data/applications.json` |
| `purchase_requests` | Заявки на покупку | `data/purchase_requests.json` |
| `task_submissions` | Отправленные задания | `data/task_submissions.json` |
| `reward_history` | История наград | `data/reward_history.json` |
| `leaderboard` | Таблица лидеров | `data/leaderboard.json` |
| `cell_tasks` | Задания для клеток | `data/cell_tasks.json` |
| `game_states` | Игровые состояния | `data/game_states.json` |
| `shop_items` | Товары магазина | `data/shop_items.json` |
| `shopping_carts` | Корзины пользователей | `data/shopping_carts.json` |

### 🔄 **Поток данных:**

```
Пользователь → JavaScript → API Клиент → Python API → JSON файлы
     ↑                                                      ↓
localStorage (backup) ← JavaScript ← API Клиент ← Python API
```

### ⚡ **Преимущества новой архитектуры:**

1. **Централизованное хранение** - все данные в JSON файлах на сервере
2. **Автоматическая синхронизация** - данные обновляются в реальном времени
3. **Надежность** - localStorage как backup при недоступности сервера
4. **Кеширование** - быстрый доступ к данным
5. **Масштабируемость** - легко добавить базу данных

### 🚀 **Запуск системы:**

#### Windows:
```bash
# Запуск API сервера
python api_server.py

# Запуск веб-сервера (в другом терминале)
python -m http.server 3000

# Или используйте скрипт
start.bat
```

#### Linux/Mac:
```bash
# Запуск API сервера
python3 api_server.py

# Запуск веб-сервера (в другом терминале)
python3 -m http.server 3000

# Или используйте скрипт
./start.sh
```

### 🧪 **Тестирование API:**

```bash
# Проверка статуса
curl http://localhost:5000/api/status

# Загрузка пользователей
curl http://localhost:5000/api/data/users

# Загрузка всех данных
curl http://localhost:5000/api/all-data
```

### 🔧 **Настройка для production:**

1. **Измените порт** в `api_server.py` и `api_client.js`
2. **Добавьте аутентификацию** для API
3. **Настройте HTTPS** для безопасности
4. **Используйте базу данных** вместо JSON файлов
5. **Добавьте логирование** и мониторинг

### 📝 **Логи в консоли браузера:**

- `🔄 Загрузка данных с сервера...` - начало загрузки
- `✅ Все данные загружены с сервера` - успешная загрузка
- `⚠️ Сервер недоступен, используем localStorage` - fallback
- `💾 Данные сохранены в localStorage` - backup сохранение
- `✅ Все данные сохранены на сервер` - успешное сохранение

---

**Теперь ваша игра работает с полноценным API сервером! 🎉**

