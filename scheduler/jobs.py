'''
jobs.py

Archivo que convierte la ejecución de Remiders en asyncrono para que pueda trabajar
con el scheduler.

Ejemplo, la tarea de ejecución diaria debería llamar directo al Reminder pero, por asyncronía,
ejecuta al daily_tasks_job, el cual convierte la llamada en asyncrona y permite ahora si llamar al ReminderService.

Si se desea incluir otro job, se debe hacer el puente desde aquí.

'''
from services.reminder_service import ReminderService
from utils.async_runner import async_runner
from utils.logger import logger


def daily_tasks_job():
    logger.info("ejecutando recordatorio de tareas diarias")
    async_runner.run(
        ReminderService.daily_tasks()
    )

def week_tasks_job():
    logger.info("ejecutando recordatorio de tareas semanales")
    async_runner.run(
        ReminderService.week_tasks()
    )

def month_tasks_job():
    logger.info("ejecutando recordatorio de tareas mensuales")
    async_runner.run(
        ReminderService.month_tasks()
    )

def clean_tasks_job():
    logger.info("ejecutando borrado de tareas")
    async_runner.run(
        ReminderService.clean_tasks()
    )

def process_reminders_job():
    logger.info("ejecutando process_reminders_job")
    async_runner.run(
        ReminderService.process_reminders()
    )