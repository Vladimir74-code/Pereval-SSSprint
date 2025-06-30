import psycopg2
from decouple import config

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config('FSTR_DB_NAME'),
            user=config('FSTR_DB_LOGIN'),
            password=config('FSTR_DB_PASS'),
            host=config('FSTR_DB_HOST'),
            port=config('FSTR_DB_PORT')
        )
        self.cursor = self.conn.cursor()

    def add_pereval(self, data):
        try:
            self.cursor.execute("""
                INSERT INTO users (email, fam, name, otc, phone)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING email;
            """, (
                data['user']['email'],
                data['user']['fam'],
                data['user']['name'],
                data['user'].get('otc', ''),
                data['user']['phone']
            ))
            user_email = self.cursor.fetchone()
            if not user_email:
                user_email = (data['user']['email'],)

            self.cursor.execute("""
                INSERT INTO coords (latitude, longitude, height)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (
                data['coords']['latitude'],
                data['coords']['longitude'],
                data['coords']['height']
            ))
            coord_id = self.cursor.fetchone()[0]

            self.cursor.execute("""
                INSERT INTO pereval_added (beauty_title, title, other_titles, connect, add_time, status, coord_id, user_email, winter, summer, autumn, spring)
                VALUES (%s, %s, %s, %s, %s, 'new', %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                data['beauty_title'],
                data['title'],
                data.get('other_titles', ''),
                data.get('connect', ''),
                data['add_time'],
                coord_id,
                user_email[0],
                data.get('winter', ''),
                data.get('summer', ''),
                data.get('autumn', ''),
                data.get('spring', '')
            ))
            pereval_id = self.cursor.fetchone()[0]

            if 'images' in data and data['images']:
                for img in data['images']:
                    self.cursor.execute("""
                        INSERT INTO pereval_images (pereval_id, image_data, title)
                        VALUES (%s, %s, %s);
                    """, (pereval_id, img['data'], img['title']))

            self.conn.commit()
            return {"status": 200, "message": "Успешно", "id": pereval_id}
        except Exception as e:
            self.conn.rollback()
            return {"status": 500, "message": str(e)}

    def get_pereval(self, id):
        try:
            self.cursor.execute(
                """
                SELECT pa.id, pa.beauty_title, pa.title, pa.other_titles, pa.connect, 
                       pa.add_time, pa.status,
                       c.latitude, c.longitude, c.height,
                       u.email, u.fam, u.name, u.otc, u.phone,
                       array_agg(pi.image_data || '|' || pi.title) as images
                FROM pereval_added pa
                JOIN coords c ON pa.coord_id = c.id
                JOIN users u ON pa.user_email = u.email
                LEFT JOIN pereval_images pi ON pa.id = pi.pereval_id
                WHERE pa.id = %s
                GROUP BY pa.id, c.id, u.email  
                """,
                (id,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_pereval(self, id, data):
        try:
            self.cursor.execute("SELECT status FROM pereval_added WHERE id = %s", (id,))
            current_status = self.cursor.fetchone()
            if not current_status or current_status[0] != 'new':
                return {"state": 0, "message": "Можно редактировать только записи со статусом 'new'"}

            update_fields = {k: v for k, v in data.items() if k not in ['user', 'email', 'fam', 'name', 'otc', 'phone']}
            if not update_fields:
                return {"state": 0, "message": "Нет данных для обновления"}

            set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
            query = f"UPDATE pereval_added SET {set_clause}, status = 'need_check' WHERE id = %s RETURNING id"
            self.cursor.execute(query, tuple(update_fields.values()) + (id,))
            if self.cursor.rowcount == 0:
                return {"state": 0, "message": "Перевал не найден"}
            self.conn.commit()
            return {"state": 1, "message": "Запись успешно обновлена"}
        except Exception as e:
            self.conn.rollback()
            return {"state": 0, "message": str(e)}

    def get_perevals_by_email(self, user__email):
        try:
            self.cursor.execute("""
                SELECT pa.*, c.latitude, c.longitude, c.height, u.email, u.fam, u.name, u.otc, u.phone,
                       array_agg(pi.image_data || '|' || pi.title) as images
                FROM pereval_added pa
                JOIN coords c ON pa.coord_id = c.id
                JOIN users u ON pa.user_email = u.email
                LEFT JOIN pereval_images pi ON pa.id = pi.pereval_id
                WHERE u.email = %s
                GROUP BY pa.id, c.id, u.email
            """, (user__email,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении перевалов: {e}")
            return []

    def __del__(self):
        self.cursor.close()
        self.conn.close()