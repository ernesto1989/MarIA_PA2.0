from database.connection import get_connection

class UserService:

    @staticmethod
    def find_user_by_id(user_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    staticmethod
    def find_admin():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role = 'ADMIN'
            AND status = 'ACTIVE'
            LIMIT 1
        """)

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        return admin


    @staticmethod
    def find_user_by_telegram(telegram_user_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE telegram_user_id = %s
        """, (telegram_user_id,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user


    @staticmethod
    def add_user(name, telegram_user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (
                telegram_user_id,
                name
            )
            VALUES
            (
                %s,
                %s
            )
        """, (
            telegram_user_id,
            name
        ))

        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return new_id


    @staticmethod
    def update_user(user_id,
                    name=None,
                    status=None):

        conn = get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if name is not None:
            updates.append("name=%s")
            values.append(name)

        if status is not None:
            updates.append("status=%s")
            values.append(status)

        if len(updates) == 0:
            return False

        values.append(user_id)

        sql = f"""
            UPDATE users
            SET {', '.join(updates)}
            WHERE id=%s
        """

        cursor.execute(sql, tuple(values))

        conn.commit()

        updated = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return updated