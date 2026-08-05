'''
activity_service.py

Gestión de actividades (tareas) del usuario.

Los métodos se desarrollan de manera estática, ya que no es necesario instanciar la clase para poder usarlos.
Adicionalmente se plantean de manera genérica (como find_tasks) con el objetivo de que el agente pueda llamarlos de manera dinámica, 
sin necesidad de conocer la firma exacta de cada método.

Se incluye:

1. Buscar una actividad por id
2. Buscar todas las actividades de un usuario
3. Búsqueda de tareas del día
4. Búsqueda de tareas de la semana
5. Búsqueda de tareas del mes
6. Agregar una nueva tarea
7. Actualizar una tarea
8. Borrado de todas las tareas

'''
from database.connection import get_connection

class ActivityService:

    #Busca una actividad por id
    @staticmethod
    def find_task(task_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM activities
            WHERE id=%s
        """, (task_id,))

        task = cursor.fetchone()

        cursor.close()
        conn.close()

        return task

    #Busca todas las actividades de un usuario, con filtros opcionales.
    @staticmethod
    def find_tasks(
        user_id,
        status=None,
        priority=None,
        due_date=None,
        due_before=None,
        due_after=None,
        limit=None
    ):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM activities
            WHERE user_id=%s
        """

        values = [user_id]

        if status is not None:
            sql += " AND status=%s"
            values.append(status)

        if priority is not None:
            sql += " AND priority=%s"
            values.append(priority)

        if due_date is not None:
            sql += " AND due_date=%s"
            values.append(due_date)

        if due_before is not None:
            sql += " AND due_date<=%s"
            values.append(due_before)

        if due_after is not None:
            sql += " AND due_date>=%s"
            values.append(due_after)

        sql += " ORDER BY due_date ASC"

        if limit is not None:
            sql += " LIMIT %s"
            values.append(limit)

        cursor.execute(sql, tuple(values))

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        return tasks

    #Método que busca las actividades del usuario que vencen hoy. Se usa para enviar recordatorios diarios.
    @staticmethod
    def find_tasks_for_today(user_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM activities
            WHERE user_id=%s AND due_date = CURDATE()
        """, (user_id,))

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        return tasks

    @staticmethod
    def find_tasks_for_this_week(user_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM activities
            WHERE user_id = %s
            AND status = 'IN_PROGRESS'
            AND due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 6 DAY)
            ORDER BY due_date ASC, priority DESC
        """, (user_id,))

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        return tasks

    @staticmethod
    def find_tasks_for_this_month(user_id):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM activities
            WHERE user_id = %s
            AND status = 'IN_PROGRESS'
            AND due_date BETWEEN CURDATE()
                            AND LAST_DAY(CURDATE())
            ORDER BY due_date ASC, priority DESC;
        """, (user_id,))

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        return tasks

    #Agrega actividades del usuario
    @staticmethod
    def add_task(user_id,
                 title,
                 due_date,
                 priority):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO activities
            (
                user_id,
                title,
                due_date,
                priority
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """, (
            user_id,
            title,
            due_date,
            priority
        ))

        conn.commit()

        task_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return task_id


    #Actualiza una actividad
    @staticmethod
    def update_task(task_id,
                    title=None,
                    due_date=None,
                    priority=None,
                    status=None):

        conn = get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if title is not None:
            updates.append("title=%s")
            values.append(title)

        if due_date is not None:
            updates.append("due_date=%s")
            values.append(due_date)

        if priority is not None:
            updates.append("priority=%s")
            values.append(priority)

        if status is not None:
            updates.append("status=%s")
            values.append(status)

        if len(updates) == 0:
            return False

        values.append(task_id)

        sql = f"""
            UPDATE activities
            SET {', '.join(updates)}
            WHERE id=%s
        """

        cursor.execute(sql, tuple(values))

        conn.commit()

        updated = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return updated

    #Elimina todas las actividades completadas
    @staticmethod
    def cleanup_completed_tasks():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc(
            "sp_cleanup_completed_tasks"
        )

        conn.commit()

        cursor.close()
        conn.close()

        return True