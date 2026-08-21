"""
reminder_service.py

Archivo que contiene todos los procesos que se ejecutarán por jobs
automáticos para notificaciones al usuario.

Se incluyen:
1. Proceso de notificación diario de tareas (para ese día)
2. Proceso de notificación semanal de tareas
3. Proceso de notificación mensual de tareas.
4. Proceso de limpieza de Base de Datos de actividades terminadas.

"""

from services.user_service import UserService
from services.tasks_service import TasksService
from database.connection import get_connection
from datetime import datetime, date, time, timedelta
from utils.logger import logger

from notifications.notifier import (
    notify_daily_tasks,
    notify_week_tasks,
    notify_month_tasks,
    notify_clean_tasks,
    notify_task_reminder,
    notify_one_shot_reminder,
    notify_recurring_reminder
)


class ReminderService:

    #Método que automatiza la búsqueda de todos las tareas de ese día de todos los usuarios. Es consumido por el job de 
    #recordatorios diarios.
    @staticmethod
    async def daily_tasks():
        try:
            # Obtener todos los usuarios activos
            users = UserService.find_active_users()

            for user in users:

                tasks = TasksService.find_tasks_for_today(
                    user["id"]
                )

                if not tasks:
                    continue

                pending_tasks = [
                    t for t in tasks
                    if t["status"] == "IN_PROGRESS"
                ]

                completed_tasks = [
                    t for t in tasks
                    if t["status"] == "COMPLETED"
                ]

                await notify_daily_tasks(
                    user,
                    pending_tasks,
                    completed_tasks
                )
        except Exception:
            logger.exception("Error ejecutando recordatorios diarios")
            raise

    #Método que automatiza la búsqueda de todos las tareas de esa semana de todos los usuarios. Es consumido por el job de 
    #recordatorios semanales.
    @staticmethod
    async def week_tasks():
        try:
            # Obtener todos los usuarios activos
            users = UserService.find_active_users()

            for user in users:

                tasks = TasksService.find_tasks_for_this_week(
                    user["id"]
                )

                if not tasks:
                    continue

                await notify_week_tasks(
                    user,
                    tasks
                )
        except Exception:
            logger.exception("Error ejecutando recordatorios semanales")
            raise

    #Método que automatiza la búsqueda de todos las tareas de ese mes de todos los usuarios. Es consumido por el job de 
    #recordatorios mensuales.
    @staticmethod
    async def month_tasks():
        try:
            # Obtener todos los usuarios activos
            users = UserService.find_active_users()

            for user in users:

                tasks = TasksService.find_tasks_for_this_month(
                    user["id"]
                )

                if not tasks:
                    continue

                await notify_month_tasks(
                    user,
                    tasks
                )
        except Exception:
            logger.exception("Error ejecutando recordatorios mensuales")
            raise

    #Método que automatiza la limpieza de base de datos buscando actividades terminadas.
    #Al finalizar, notifica al usuario administrador el cumplimiento de la tarea.
    @staticmethod
    async def clean_tasks():
        try:
            TasksService.cleanup_completed_tasks()
            await notify_clean_tasks()
        except Exception:
            logger.exception("Error ejecutando limpieza de tareas completadas")
            raise

    # reminders!!!

    #Cuando el usuario pida sus reminders... (para administrar)
    @staticmethod
    def find_user_reminders(
        user_id: int
    ) -> list:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    r.*
                FROM reminders r
                WHERE r.user_id = %s
                ORDER BY
                    r.reminder_type,
                    r.frequency,
                    r.trigger_time
                """,
                (user_id,)
            )

            reminders = cursor.fetchall()
            # Agregar weekdays a los reminders semanales
            for reminder in reminders:
                if reminder["frequency"] == "WEEKLY":
                    cursor.execute(
                        """
                        SELECT weekday
                        FROM reminder_weekdays
                        WHERE reminder_id = %s
                        ORDER BY weekday
                        """,
                        (reminder["id"],)
                    )
                    reminder["weekdays"] = [
                        row["weekday"]
                        for row in cursor.fetchall()
                    ]
            return reminders
        except Exception as e:
            logger.exception(
                f"Error obteniendo reminders del usuario {user_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def find_due_task_reminders() -> list:

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    r.*,
                    a.title,
                    a.due_date,
                    a.due_time,
                    a.priority,
                    u.telegram_user_id

                FROM reminders r

                INNER JOIN tasks a
                    ON a.id = r.activity_id

                INNER JOIN users u
                    ON u.id = r.user_id

                WHERE r.reminder_type = 'TASK'
                AND r.enabled = TRUE

                AND a.status = 'IN_PROGRESS'
                AND a.due_date IS NOT NULL
                AND a.due_time IS NOT NULL

                AND DATE_SUB(
                        TIMESTAMP(a.due_date, a.due_time),
                        INTERVAL r.remind_before_minutes MINUTE
                    )
                    BETWEEN
                        DATE_SUB(NOW(), INTERVAL 1 MINUTE)
                        AND NOW()

                ORDER BY
                    a.due_date,
                    a.due_time;
                """
            )

            return cursor.fetchall()
        except Exception:
            logger.exception(
                "Error obteniendo reminders TASK."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def find_due_one_shot_reminders() -> list:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT 
                    u.telegram_user_id ,
                    r.*
                FROM reminders r
                join users u on u.id = r.user_id 
                WHERE reminder_type = 'ONE_SHOT'
                AND enabled = TRUE
                AND trigger_date = CURDATE()
                AND trigger_time <= CURTIME()
                ORDER BY trigger_time
                """
            )
            return cursor.fetchall()
        except Exception:
            logger.exception(
                "Error obteniendo reminders ONE_SHOT."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()   

    @staticmethod
    def find_due_recurring_reminders() -> list:
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT DISTINCT
                    u.telegram_user_id,
                    r.*
                FROM reminders r
                JOIN users u on u.id = r.user_id
                LEFT JOIN reminder_weekdays rw ON rw.reminder_id = r.id
                WHERE r.reminder_type = 'RECURRING'
                AND r.enabled = TRUE
                AND r.trigger_time <= CURTIME()
                AND (
                    -- Reminder que ya ha sido enviado anteriormente
                    (
                        -- aqui es solo true si ya fue enviado (last_sent_at no es null) y fue enviado antes que hoy
                        r.last_sent_at IS NOT NULL
                        AND DATE(r.last_sent_at) < CURDATE()
                    )
                    OR
                    -- Primer envío: solo si fue creado antes de la hora programada de hoy
                    (
                        -- es nuevo (no ha sido enviado) y la hora la que ha sido creado no ha pasado
                        -- aquí, por ejemplo si lo creo a las 12 y se debe ejecutar a la una, apenas lo enviará
                        -- si lo creo y ya pasó la hora diaria, ya no lo envia
                        r.last_sent_at IS NULL
                        AND r.created_at <= TIMESTAMP(CURDATE(), r.trigger_time)
                    )
                )
                AND (
                        r.frequency = 'DAILY'
                        OR
                        (
                            r.frequency = 'WEEKLY'
                            AND rw.weekday = WEEKDAY(CURDATE()) + 1
                        )
                        OR
                        (
                            r.frequency = 'MONTHLY'
                            AND r.day_of_month = DAY(CURDATE())
                        )
                        OR
                        (
                            r.frequency = 'YEARLY'
                            AND r.day_of_month = DAY(CURDATE())
                            AND r.month_of_year = MONTH(CURDATE())
                        )
                )
                ORDER BY
                    r.trigger_time;
                """
            )
            return cursor.fetchall()
        except Exception:
            logger.exception(
                "Error obteniendo reminders RECURRING."
            )
            raise

        finally:
            if cursor:cursor.close()
            if conn:conn.close()

    @staticmethod
    def add_task_reminder(
        user_id: int,
        activity_id: int,
        remind_before_minutes: int
    ) -> int:
        conn = None
        cursor = None      
        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO reminders
                (
                    user_id,
                    activity_id,
                    reminder_type,
                    trigger_time,
                    remind_before_minutes
                )
                VALUES
                (
                    %s,
                    %s,
                    'TASK',
                    '00:00:00', 
                    %s
                )
                """,
                (
                    user_id,
                    activity_id,
                    remind_before_minutes
                )
            )

            reminder_id = cursor.lastrowid
            conn.commit()
            logger.info(
                f"Reminder TASK {reminder_id} creado para activity {activity_id}."
            )
            return reminder_id

        except Exception:
            if conn: conn.rollback()
            logger.exception(
                f"Error creando reminder para activity {activity_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def add_one_shot_reminder(
        user_id: int,
        title: str,
        trigger_date: date,
        trigger_time: time
    ) -> int:
        
        conn = None
        cursor = None

        logger.info("Entró a ReminderService.add_one_shot_reminder")

        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            logger.info(
                f"INSERT -> {user_id}, {title}, {trigger_date}, {trigger_time}"
            )

            cursor.execute(
                """
                INSERT INTO reminders
                (
                    user_id,
                    title,
                    reminder_type,
                    trigger_date,
                    trigger_time
                )
                VALUES
                (
                    %s,
                    %s,
                    'ONE_SHOT',
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    title,
                    trigger_date,
                    trigger_time
                )
            )
            logger.info("INSERT ejecutado")
            reminder_id = cursor.lastrowid
            conn.commit()
            logger.info(
                f"Reminder ONE_SHOT {reminder_id} creado para usuario {user_id}."
            )
            return reminder_id
        except Exception:
            if conn: conn.rollback()
            logger.exception(
                f"Error creando reminder ONE_SHOT para usuario {user_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    
    @staticmethod
    def add_recurring_reminder(
        user_id: int,
        title: str,
        frequency: str,
        trigger_time: time,
        weekdays: list[int] = None,
        day_of_month: int = None,
        month_of_year: int = None
    ) -> int:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO reminders
                (
                    user_id,
                    title,
                    reminder_type,
                    frequency,
                    trigger_time,
                    day_of_month,
                    month_of_year
                )
                VALUES
                (
                    %s,
                    %s,
                    'RECURRING',
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    title,
                    frequency,
                    trigger_time,
                    day_of_month,
                    month_of_year
                )
            )

            reminder_id = cursor.lastrowid
            # Si es semanal, registrar los días
            if frequency == "WEEKLY" and weekdays:
                for weekday in weekdays:
                    cursor.execute(
                        """
                        INSERT INTO reminder_weekdays
                        (
                            reminder_id,
                            weekday
                        )
                        VALUES
                        (
                            %s,
                            %s
                        )
                        """,
                        (
                            reminder_id,
                            weekday
                        )
                    )
            conn.commit()
            logger.info(
                f"Reminder RECURRING {reminder_id} creado para usuario {user_id}."
            )
            return reminder_id
        except Exception:
            if conn:conn.rollback()
            logger.exception(
                f"Error creando reminder RECURRING para usuario {user_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def disable_reminder(
        reminder_id: int
    ):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE reminders
                SET enabled = FALSE
                WHERE id = %s
                """,
                (reminder_id,)
            )

            conn.commit()

            logger.info(
                f"Reminder {reminder_id} deshabilitado."
            )

        except Exception:
            if conn:
                conn.rollback()

            logger.exception(
                f"Error deshabilitando reminder {reminder_id}."
            )
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def update_reminder(
        reminder_id: int,
        title: str = None,
        trigger_date: date = None,
        trigger_time: time = None,
        frequency: str = None,
        day_of_month: int = None,
        month_of_year: int = None,
        enabled: bool = None
    ):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            fields = []
            values = []

            if title is not None:
                fields.append("title = %s")
                values.append(title)

            if trigger_date is not None:
                fields.append("trigger_date = %s")
                values.append(trigger_date)

            if trigger_time is not None:
                fields.append("trigger_time = %s")
                values.append(trigger_time)

            if frequency is not None:
                fields.append("frequency = %s")
                values.append(frequency)

            if day_of_month is not None:
                fields.append("day_of_month = %s")
                values.append(day_of_month)

            if month_of_year is not None:
                fields.append("month_of_year = %s")
                values.append(month_of_year)

            if enabled is not None:
                fields.append("enabled = %s")
                values.append(enabled)

            if not fields:
                return
            values.append(reminder_id)

            cursor.execute(
                f"""
                UPDATE reminders
                SET {", ".join(fields)}
                WHERE id = %s
                """,
                values
            )

            conn.commit()

            logger.info(
                f"Reminder {reminder_id} actualizado."
            )

        except Exception:
            if conn: conn.rollback()

            logger.exception(
                f"Error actualizando reminder {reminder_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    @staticmethod
    def delete_reminder(
        reminder_id: int
    ):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM reminders
                WHERE id = %s
                """,
                (reminder_id,)
            )

            conn.commit()

            logger.info(
                f"Reminder {reminder_id} eliminado."
            )

        except Exception:
            if conn: conn.rollback()

            logger.exception(
                f"Error eliminando reminder {reminder_id}."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    @staticmethod
    async def process_reminders():
        logger.info("Procesando reminders...")

        task_reminders = ReminderService.find_due_task_reminders()
        for reminder in task_reminders:
            try:
                await notify_task_reminder(reminder)
                ReminderService.disable_reminder(
                    reminder["id"]
                )
            except Exception:
                logger.exception(
                    f"Error enviando TASK reminder {reminder['id']}."
                )

        one_shot_reminders = ReminderService.find_due_one_shot_reminders()
        for reminder in one_shot_reminders:
            try:
                await notify_one_shot_reminder(reminder)
                ReminderService.disable_reminder(
                    reminder["id"]
                )
            except Exception:
                logger.exception(
                    f"Error enviando ONE_SHOT reminder {reminder['id']}."
                )

        recurring_reminders = ReminderService.find_due_recurring_reminders()
        for reminder in recurring_reminders:
            try:
                await notify_recurring_reminder(reminder)
                ReminderService.mark_as_sent(
                    reminder["id"]
                )
            except Exception:

                logger.exception(
                    f"Error enviando RECURRING reminder {reminder['id']}."
                )


    @staticmethod
    def mark_as_sent(
        reminder_id: int
    ):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            conn.start_transaction()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE reminders
                SET
                    last_sent_at = NOW()
                WHERE id = %s
                """,
                (reminder_id,)
            )

            conn.commit()
            logger.info(
                f"Reminder {reminder_id} marcado como enviado."
            )
        except Exception:
            if conn: conn.rollback()
            logger.exception(
                f"Error marcando reminder {reminder_id} como enviado."
            )
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()