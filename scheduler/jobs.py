'''
jobs.py

Archivo que convierte la ejecución de Remiders en asyncrono para que pueda trabajar
con el scheduler.

Ejemplo, la tarea de ejecución diaria debería llamar directo al Reminder pero, por asyncronía,
ejecuta al daily_tasks_job, el cual convierte la llamada en asyncrona y permite ahora si llamar al ReminderService.

Si se desea incluir otro job, se debe hacer el puente desde aquí.

'''
from services.reminder_service import ReminderService

import asyncio


def daily_tasks_job():

    asyncio.run(
        ReminderService.daily_tasks()
    )

def week_tasks_job():

    asyncio.run(
        ReminderService.week_tasks()
    )

def month_tasks_job():
    
    asyncio.run(
        ReminderService.month_tasks()
    )

def clean_tasks_job():
    
    asyncio.run(
        ReminderService.clean_tasks()
    )