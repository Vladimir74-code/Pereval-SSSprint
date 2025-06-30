# Pereval Project (FastAPI)

## Описание задачи
Проект представляет собой REST API для управления данными о перевалах (горных маршрутах). Задача включала разработку двух спринтов:
- **Спринт 1**: Реализация базового API для добавления данных о перевалах с использованием FastAPI и PostgreSQL.
- **Спринт 2**: Расширение API новыми методами для получения, редактирования и фильтрации данных.

## Что реализовано
- **Класс для работы с БД**: Создан класс `DBManager` для взаимодействия с PostgreSQL (добавление, получение, обновление данных).
- **REST API (Спринт 1)**:
  - `POST /submitData`: Добавление новой записи о перевале.
- **REST API (Спринт 2)**:
  - `GET /submitData/<id>`: Получение записи по ID с полями, включая статус модерации.
  - `PATCH /submitData/<id>`: Редактирование записи (только для статуса "new", без изменения ФИО, email, телефона).
  - `GET /submitData/?user__email=<email>`: Получение списка записей по email пользователя.
- **Переменные окружения**: Подключение к базе через `.env` (FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS).
- **Структура БД**: Таблицы `users`, `coords`, `pereval_added`, `pereval_images` с внешними ключами.

## Как работать с API
1. **Установка**:
   - Клонируй репозиторий: `git clone https://github.com/Vladimir74-code/Pereval-SSSprint.git`.
   - Создай виртуальное окружение: `python -m venv venv`.
   - Активируй: `.\venv\Scripts\activate` (Windows).
   - Установи зависимости: `pip install -r requirements.txt`.
   - Настрой `.env` с данными базы данных.
2. **Запуск**:
   - Запусти сервер: `python -m pereval_app.api`.
   - API будет доступно на `http://127.0.0.1:8000`.
3. **Примеры запросов (локально)**:
   - **POST /submitData**:
     ```bash
     curl -X POST "http://127.0.0.1:8000/submitData" -H "Content-Type: application/json" -d "{\"beauty_title\":\"пер. Пхия\",\"title\":\"Пхия\",\"other_titles\":\"Триев\",\"connect\":\"\",\"add_time\":\"2021-09-22 13:18:13\",\"user\":{\"email\":\"qwerty@mail.ru\",\"fam\":\"Пупкин\",\"name\":\"Василий\",\"otc\":\"Иванович\",\"phone\":\"+7 555 55 55\"},\"coords\":{\"latitude\":\"45.3842\",\"longitude\":\"7.1525\",\"height\":1200},\"images\":[{\"data\":\"<картинка1>\",\"title\":\"Седловина\"}]}"
Ответ: {"status": 200, "message": "Отправлено успешно", "id": <id>}.

--GET /submitData/<id></id>:
bash


curl http://127.0.0.1:8000/submitData/1
Ответ: JSON с данными перевала.


--PATCH /submitData/<id></id>:
bash


curl -X PATCH "http://127.0.0.1:8000/submitData/1" -H "Content-Type: application/json" -d "{\"beauty_title\":\"пер. Новый Пхия\"}"
Ответ: {"state": 1, "message": "Запись успешно обновлена"}.


--GET /submitData/?user__email=<email></email>:
bash

curl "http://127.0.0.1:8000/submitData/?user__email=qwerty@mail.ru"

Ответ: Массив JSON-объектов.

Тестирование: Используй Postman для отправки запросов и проверки ответов.
Дополнительно:
Код следует PEP 8 (проверено с помощью flake8).
Использован Git с веткой submitData для разработки.

Ссылка на репозиторий
GitHub: https://github.com/Vladimir74-code/Pereval-SSSprint.git

## Документация Swagger
Автоматическая документация доступна при запуске сервера. Открой `http://127.0.0.1:8000/docs` в браузере для тестирования API.