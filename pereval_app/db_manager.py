import psycopg2
from decouple import config

class DBManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=config('FSTR_DB_NAME'),
                user=config('FSTR_DB_LOGIN'),
                password=config('FSTR_DB_PASS'),
                host=config('FSTR_DB_HOST'),
                port=config('FSTR_DB_PORT')
            )
            print("Подключение успешно!")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения: {str(e)}")
            raise

    def add_pereval(self, data):
        user_data = data.get('user', {})
        coords_data = data.get('coords', {})
        images_data = data.get('images', [])
        try:
            self.cursor.execute(
                "INSERT INTO users (email, fam, name, otc, phone) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
                (user_data.get('email'), user_data.get('fam'), user_data.get('name'),
                 user_data.get('otc'), user_data.get('phone'))
            )
            self.cursor.execute(
                "INSERT INTO coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id",
                (coords_data.get('latitude'), coords_data.get('longitude'), coords_data.get('height'))
            )
            coord_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                "INSERT INTO pereval_added (beauty_title, title, other_titles, connect, add_time, status, coord_id, user_email, winter, summer, autumn, spring) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (data.get('beauty_title'), data.get('title'), data.get('other_titles'),
                 data.get('connect'), data.get('add_time'), 'new', coord_id,
                 user_data.get('email'), data.get('winter', ''), data.get('summer', ''),
                 data.get('autumn', ''), data.get('spring', ''))
            )
            pereval_id = self.cursor.fetchone()[0]
            for image in images_data:
                self.cursor.execute(
                    "INSERT INTO pereval_images (pereval_id, image_data, title) VALUES (%s, %s, %s)",
                    (pereval_id, image.get('data'), image.get('title'))
                )
            self.conn.commit()
            return {'status': 200, 'message': 'Успешно добавлено', 'id': pereval_id}
        except Exception as e:
            self.conn.rollback()
            return {'status': 500, 'message': str(e), 'id': None}

    def get_pereval(self, id):
        try:
            self.cursor.execute(
                """
                SELECT p.id, p.beauty_title, p.title, p.other_titles, p.connect, p.add_time, p.status,
                       c.latitude, c.longitude, c.height,
                       u.email, u.fam, u.name, u.otc, u.phone,
                       array_agg(i.image_data || '|' || i.title) as images
                FROM pereval_added p
                JOIN coords c ON p.coord_id = c.id
                JOIN users u ON p.user_email = u.email
                LEFT JOIN pereval_images i ON p.id = i.pereval_id
                WHERE p.id = %s
                GROUP BY p.id, c.id, u.email
                """,
                (id,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            raise e

    def get_perevals_by_email(self, email):
        try:
            self.cursor.execute(
                """
                SELECT p.id, p.beauty_title, p.title, p.other_titles, p.connect, p.add_time, p.status,
                       c.latitude, c.longitude, c.height,
                       u.email, u.fam, u.name, u.otc, u.phone,
                       array_agg(i.image_data || '|' || i.title) as images
                FROM pereval_added p
                JOIN coords c ON p.coord_id = c.id
                JOIN users u ON p.user_email = u.email
                LEFT JOIN pereval_images i ON p.id = i.pereval_id
                WHERE u.email = %s
                GROUP BY p.id, c.id, u.email
                """,
                (email,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_pereval(self, id, data):
        try:
            self.cursor.execute("SELECT status FROM pereval_added WHERE id = %s", (id,))
            status = self.cursor.fetchone()
            if not status or status[0] != 'new':
                return {'state': 0, 'message': 'Редактирование возможно только для статуса "new"'}
            allowed_fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'winter', 'summer', 'autumn', 'spring']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not update_data:
                return {'state': 0, 'message': 'Нет данных для обновления или изменены запрещённые поля'}
            set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
            self.cursor.execute(
                f"UPDATE pereval_added SET {set_clause}, add_time = %s WHERE id = %s",
                tuple(update_data.values()) + (data.get('add_time', ''), id)
            )
            self.conn.commit()
            return {'state': 1, 'message': 'Запись успешно обновлена'}
        except Exception as e:
            self.conn.rollback()
            return {'state': 0, 'message': f'Ошибка при обновлении: {str(e)}'}

    def __del__(self):
        self.cursor.close()
        self.conn.close()