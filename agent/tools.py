'''
 Este archivo contiene herramientas para interactuar con las actividades del usuario.
 Crea funciones que le dan funciones al agente.
'''
from agents import function_tool
from services.activity_service import ActivityService
from services.reminder_service import ReminderService
from datetime import datetime
from utils.logger import logger

def build_find_tasks_tool(user_id):

    @function_tool
    def find_tasks():
        """
        Obtiene todas las actividades del usuario.
        """

        tasks = ActivityService.find_tasks(user_id)

        return tasks

    return find_tasks

def build_find_task_tool(user_id):

    @function_tool
    def find_task(task_id: int):
        """
        Obtiene una actividad específica del usuario mediante su ID.
        Utilízala cuando el usuario haga referencia a una actividad concreta.
        """

        task = ActivityService.find_task(task_id)

        if task is None:
            return "Actividad no encontrada."

        if task["user_id"] != user_id:
            return "La actividad no pertenece al usuario."

        return task

    return find_task

def build_add_task_tool(user_id):

    @function_tool
    def add_task(
        title: str,
        due_date: str,
        due_time: str,
        priority: str
    ):
        """
        Crea una nueva actividad.

        priority debe ser:
        LOW
        MEDIUM
        URGENT
        """

        task_id = ActivityService.add_task(
            user_id,
            title,
            due_date,
            due_time,
            priority
        )

        return f"Actividad creada correctamente. Id={task_id}"
    
    return add_task


def build_update_task_tool(user_id):

    @function_tool
    def update_task(
        task_id: int,
        title: str = None,
        due_date: str = None,
        due_time: str = None,
        priority: str = None,
        status: str = None
    ):
        """
        Actualiza una actividad existente.
        """

        task = ActivityService.find_task(task_id)

        if task is None:
            return "Actividad no encontrada."

        if task["user_id"] != user_id:
            return "La actividad no pertenece al usuario."

        updated = ActivityService.update_task(
            task_id,
            title,
            due_date,
            due_time,
            priority,
            status
        )

        return "Actividad actualizada." if updated else "No hubo cambios."

    return update_task


def build_cleanup_completed_tasks_tool(user_id):

    @function_tool
    def cleanup_completed_tasks():
        """
        Elimina todas las actividades terminadas del usuario.
        """

        ActivityService.cleanup_completed_tasks(
            user_id
        )

        return "Las actividades terminadas fueron eliminadas."

    return cleanup_completed_tasks


def build_add_task_reminder_tool(user_id: int):

    @function_tool
    async def add_task_reminder(
        activity_id: int,
        remind_before_minutes: int
    ) -> str:
        """
        Crea un recordatorio asociado a una tarea.
        """

        logger.info("TOOL add_task_reminder(...)")

        ReminderService.add_task_reminder(
            user_id=user_id,
            activity_id=activity_id,
            remind_before_minutes=remind_before_minutes
        )

        return "Recordatorio de tarea creado correctamente."

    return add_task_reminder

def build_add_one_shot_reminder_tool(user_id: int):

    @function_tool
    async def add_one_shot_reminder(
        title: str,
        trigger_date: str,
        trigger_time: str
    ) -> str:
        """
        Crea un recordatorio que se ejecutará una sola vez.
        trigger_date debe venir en formato YYYY-MM-DD.
        trigger_time debe venir en formato HH:MM.
        """

        logger.info(f"TOOL add_one_shot_reminder")

        trigger_date = datetime.strptime(trigger_date,"%Y-%m-%d").date()
        trigger_time = trigger_time=datetime.strptime(trigger_time,"%H:%M").time()

        logger.info(ReminderService)
        logger.info(ReminderService.add_one_shot_reminder)

        ReminderService.add_one_shot_reminder(
            user_id=user_id,
            title=title,
            trigger_date=trigger_date,
            trigger_time=trigger_time
        )

        logger.info(f"END add_one_shot_reminder")

        return "Recordatorio creado correctamente."

    return add_one_shot_reminder

def build_add_recurring_reminder_tool(user_id: int):
    @function_tool
    async def add_recurring_reminder(
        title: str,
        frequency: str,
        trigger_time: str,
        weekdays: list[int] = None,
        day_of_month: int = None,
        month_of_year: int = None
    ) -> str:
        """
        Crea un recordatorio recurrente.

        frequency:
            DAILY
            WEEKLY
            MONTHLY
            YEARLY
        """

        logger.info("TOOL add_recurring_reminder(...)")
        trigger_time=datetime.strptime(trigger_time,"%H:%M").time()

        ReminderService.add_recurring_reminder(
            user_id=user_id,
            title=title,
            frequency=frequency,
            trigger_time=trigger_time,
            weekdays=weekdays,
            day_of_month=day_of_month,
            month_of_year=month_of_year
        )

        return "Recordatorio recurrente creado correctamente."

    return add_recurring_reminder


def build_find_reminders_tool(user_id: int):

    @function_tool
    def find_reminders() -> str:
        """
        Obtiene todos los recordatorios del usuario.
        Incluye recordatorios activos y deshabilitados.
        """

        logger.info("TOOL find_reminders(...)")

        reminders = ReminderService.find_user_reminders(user_id)

        if not reminders:
            return "No tienes recordatorios."

        return reminders

    return find_reminders

def build_disable_reminder_tool(user_id: int):

    @function_tool
    def disable_reminder(
        reminder_id: int
    ) -> str:
        """
        Deshabilita un recordatorio existente.

        Utilízalo cuando el usuario quiera dejar de recibir
        un recordatorio sin eliminarlo.
        """

        logger.info(
            f"TOOL disable_reminder({reminder_id})"
        )

        reminders = ReminderService.find_user_reminders(user_id)

        reminder = next(
            (
                r for r in reminders
                if r["id"] == reminder_id
            ),
            None
        )

        if reminder is None:
            return "No encontré ese recordatorio."

        ReminderService.disable_reminder(
            reminder_id
        )

        return "Recordatorio deshabilitado correctamente."

    return disable_reminder


def build_update_reminder_tool(user_id: int):

    @function_tool
    def update_reminder(
        reminder_id: int,
        title: str = None,
        trigger_date: str = None,
        trigger_time: str = None,
        frequency: str = None,
        day_of_month: int = None,
        month_of_year: int = None,
        enabled: bool = None
    ) -> str:
        """
        Actualiza un recordatorio existente.

        Solo modifica los campos proporcionados.

        trigger_date debe usar YYYY-MM-DD.
        trigger_time debe usar HH:MM.

        frequency puede ser:
        DAILY
        WEEKLY
        MONTHLY
        YEARLY
        """

        logger.info(
            f"TOOL update_reminder({reminder_id})"
        )

        reminders = ReminderService.find_user_reminders(user_id)

        reminder = next(
            (
                r for r in reminders
                if r["id"] == reminder_id
            ),
            None
        )

        if reminder is None:
            return "No encontré ese recordatorio."

        if trigger_date is not None:
            trigger_date = datetime.strptime(
                trigger_date,
                "%Y-%m-%d"
            ).date()

        if trigger_time is not None:
            trigger_time = datetime.strptime(
                trigger_time,
                "%H:%M"
            ).time()

        ReminderService.update_reminder(
            reminder_id=reminder_id,
            title=title,
            trigger_date=trigger_date,
            trigger_time=trigger_time,
            frequency=frequency,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            enabled=enabled
        )

        return "Recordatorio actualizado correctamente."

    return update_reminder

def build_delete_reminder_tool(user_id: int):

    @function_tool
    def delete_reminder(
        reminder_id: int
    ) -> str:
        """
        Elimina permanentemente un recordatorio.

        Utilízalo únicamente cuando el usuario quiera
        eliminarlo, no cuando solamente quiera desactivarlo.
        """

        logger.info(
            f"TOOL delete_reminder({reminder_id})"
        )

        reminders = ReminderService.find_user_reminders(user_id)

        reminder = next(
            (
                r for r in reminders
                if r["id"] == reminder_id
            ),
            None
        )

        if reminder is None:
            return "No encontré ese recordatorio."

        ReminderService.delete_reminder(
            reminder_id
        )

        return "Recordatorio eliminado correctamente."

    return delete_reminder