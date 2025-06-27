# Проект: Мобильное приложение для ФСТР (1-й спринт)

REST API для обработки данных о горных перевалах от туристов
- Python 3.11+
- FastAPI
- PostgreSQL 15
- SQLAlchemy (опционально)
- Pydantic (валидация данных)
- Uvicorn (ASGI-сервер)
- Git (ветка `submitData`)

## 🚀 Функционал
✅ Прием данных о перевалах в формате JSON  
✅ Валидация входных данных  
✅ Хранение в реляционной БД (PostgreSQL)  
✅ Автоматическое присвоение статуса `new`  
✅ Обработка ошибок (400, 500)  
✅ Поддержка Swagger-документации  

## ⚙️ Установка
1. Клонировать репозиторий:
   ```bash
   git clone -b submitData https://github.com/your-username/pereval-project.git
   cd pereval-project

 Создать и активировать виртуальное окружение:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate  # Windows
Установить зависимости:
pip install -r requirements.txt

🏃 Запуск
Настроить переменные окружения (создать файл .env):
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_NAME=pereval_db
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=yourpassword


Запустить сервер:
uvicorn pereval_app.api:app --reload

POST /submitData
Назначение: Добавление данных о новом перевале

Тело запроса: JSON 

Ответ:
{
  "status": 200,
  "message": "Отправлено успешно",
  "id": 42
}
json
{
  "status": 200,
  "message": "Отправлено успешно",
  "id": 42
}

🗃 Структура БД

Основные таблицы:

users - данные пользователей

pereval_added - информация о перевалах

coords - географические координаты

pereval_images - связь перевалов и изображений

📋 Примеры запросов

Запрос:
curl -X POST "http://localhost:8000/submitData" \
-H "Content-Type: application/json" \
-d @sample_request.json
Файл sample_request.json:
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "user": {
    "email": "user@example.com",
    "fam": "Иванов",
    "name": "Петр",
    "phone": "+79211234567"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  }
}

Разработчику
Требования к коммитам:
Соответствие PEP8

Критерии оценки:
Критерий	Баллы
Рабочий REST API	15
Качество кода	5
Работа с Git	5
Улучшенная структура БД	10

Проект разработан в рамках виртуальной стажировки.






