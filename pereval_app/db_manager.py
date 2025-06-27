import psycopg2
from decouple import config

class DBManager:
    def __init__(self):
        # Подключение к базе данных из переменных окружения
        self.conn = psycopg2.connect(
            dbname=config('FSTR_DB_NAME', default='pereval_db'),
            user=config('FSTR_DB_LOGIN', default='postgres'),
            password=config('FSTR_DB_PASS', default='123vova456'),
            host=config('FSTR_DB_HOST', default='localhost'),
            port=config('FSTR_DB_PORT', default='5432')
        )
        self.cursor = self.conn.cursor()

    def add_pereval(self, data):
        user_data = data.get('user', {})
        coords_data = data.get('coords', {})
        images_data = data.get('images', [])

        try:
            self.cursor.execute(
                """
                INSERT INTO users (email, fam, name, otc, phone)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                """,
                (user_data.get('email'), user_data.get('fam'), user_data.get('name'),
                 user_data.get('otc'), user_data.get('phone'))
            )

            self.cursor.execute(
                """
                INSERT INTO coords (latitude, longitude, height)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (coords_data.get('latitude'), coords_data.get('longitude'), coords_data.get('height'))
            )
            coord_id = self.cursor.fetchone()[0]

            self.cursor.execute(
                """
                INSERT INTO pereval_added (beauty_title, title, other_titles, connect, add_time, status, coord_id, user_email, winter, summer, autumn, spring)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (data.get('beauty_title'), data.get('title'), data.get('other_titles'),
                 data.get('connect'), data.get('add_time'), 'new',
                 coord_id, user_data.get('email'),
                 data.get('winter', ''), data.get('summer', ''), data.get('autumn', ''), data.get('spring', ''))
            )
            pereval_id = self.cursor.fetchone()[0]

            for image in images_data:
                self.cursor.execute(
                    """
                    INSERT INTO pereval_images (pereval_id, image_data, title)
                    VALUES (%s, %s, %s)
                    """,
                    (pereval_id, image.get('data').encode(), image.get('title'))
                )

            self.conn.commit()
            return {'status': 200, 'message': 'Отправлено успешно', 'id': pereval_id}

        except Exception as e:
            self.conn.rollback()
            return {'status': 500, 'message': str(e), 'id': None}

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