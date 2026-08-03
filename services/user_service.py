from database.connection import get_connection

class UserService:

    #Método que busca un usuario por su id en la base de datos.
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

    #método que ubica al usuario admin (ECV). Se utiliza para solicitar autorización de nuevos registros.
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

    # Método que busca un usuario por su id de Telegram en la base de datos.
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

    #Metodo que agrega un nuevo usuario a la base de datos. Se le da el nombre y el id de Telegram del usuario.
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

    #Metodo que actualiza la información de un usuario en la base de datos. Se le puede dar un nuevo nombre y/o un nuevo estado.
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