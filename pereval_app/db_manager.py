import psycopg2
from decouple import config

# Класс для управления данными перевалов в базе данных PostgreSQL
class DBManager:
    def __init__(self):
        # Инициализация подключения к БД с использованием переменных окружения
        self.conn = psycopg2.connect(
            dbname=config('FSTR_DB_NAME', default='pereval_db'),
            user=config('FSTR_DB_LOGIN', default='postgres'),
            password=config('FSTR_DB_PASS', default='123vova456'),
            host=config('FSTR_DB_HOST', default='localhost'),
            port=config('FSTR_DB_PORT', default='5432')
        )
        self.cursor = self.conn.cursor()

    # Добавляет перевал в базу данных с обработкой ошибок
    def add_pereval(self, data):
        user_data = data.get('user', {})
        coords_data = data.get('coords', {})
        images_data = data.get('images', [])

        try:
            # Вставка данных пользователя
            self.cursor.execute(
                """
                INSERT INTO users (email, fam, name, otc, phone)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                """,
                (user_data.get('email'), user_data.get('fam'), user_data.get('name'),
                 user_data.get('otc'), user_data.get('phone'))
            )
            # ... (остальной код без изменений)
        except Exception as e:
            self.conn.rollback()
            return {'status': 500, 'message': str(e), 'id': None}

    # Закрытие соединения при удалении объекта
    def __del__(self):
        self.cursor.close()
        self.conn.close()

# Пример использования (для теста)
if __name__ == "__main__":
    db = DBManager()
    sample_data = {
        "beauty_title": "пер. ",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "add_time": "2021-09-22 13:18:13",
        "user": {
            "email": "qwerty@mail.ru",
            "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович",
            "phone": "+7 555 55 55"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "images": [{"data": "<картинка1>", "title": "Седловина"}]
    }
    result = db.add_pereval(sample_data)
    print(result)