'''
scheduler.py

Archivo que contiene la creación del servicio de Programación de Tareas.
De momento crea 4 tareas:

1. Busqueda diaria de tareas
2. Búsqueda semanal de tareas
3. Búsqueda mensual de tareas.
4. Borrado de tareas terminadas

'''
from apscheduler.schedulers.background import BackgroundScheduler
from zoneinfo import ZoneInfo
from .jobs import daily_tasks_job, week_tasks_job, month_tasks_job,clean_tasks_job

scheduler = BackgroundScheduler(
    timezone=ZoneInfo("America/Mexico_City")
)


def start_scheduler():

    #Recordatorio diario de tareas pendientes
    scheduler.add_job(
        daily_tasks_job,
        trigger="cron",
        hour=6,
        minute=30,
        id="daily_tasks",
        replace_existing=True,
        misfire_grace_time=300
    )

    #Recordatorio semanal de tareas pendientes
    scheduler.add_job(
        week_tasks_job,
        trigger="cron",
        day_of_week="mon",
        hour=6,
        minute=30,
        id="week_tasks",
        replace_existing=True,
        misfire_grace_time=300
    )

    #Recordatorio mensual de tareas pendientes
    scheduler.add_job(
        month_tasks_job,
        trigger="cron",
        day=1,
        hour=10,
        minute=30,
        id="month_tasks",
        replace_existing=True,
        misfire_grace_time=300
    )

    #Borrado de actividades de la semana anterior.
    scheduler.add_job(
        clean_tasks_job,
        trigger="cron",
        day_of_week="mon",
        hour=23,
        minute=30,
        id="clean_tasks",
        replace_existing=True,
        misfire_grace_time=300
    )

    scheduler.start()

    print("Scheduler iniciado.")