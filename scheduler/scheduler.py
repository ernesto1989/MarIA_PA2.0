from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import daily_tasks_job, week_tasks_job, month_tasks_job,clean_tasks_job

scheduler = BackgroundScheduler()


def start_scheduler():

    #Recordatorio diario de tareas pendientes
    scheduler.add_job(
        daily_tasks_job,
        trigger="cron",
        hour=7,
        minute=0,
        id="daily_tasks",
        replace_existing=True
    )

    #Recordatorio semanal de tareas pendientes
    scheduler.add_job(
        week_tasks_job,
        trigger="cron",
        day_of_week="mon",
        hour=6,
        minute=30,
        id="week_tasks",
        replace_existing=True
    )

    #Recordatorio mensual de tareas pendientes
    scheduler.add_job(
        month_tasks_job,
        trigger="cron",
        day=1,
        hour=6,
        minute=30,
        id="month_tasks",
        replace_existing=True
    )

    # scheduler.add_job(
    #     clean_tasks_job,
    #     trigger="cron",
    #     day=1,
    #     hour=6,
    #     minute=30,
    #     id="clean_tasks",
    #     replace_existing=True
    # )
    scheduler.add_job(
        clean_tasks_job,
        trigger="cron",
        hour=7,
        minute=0,
        id="clean_tasks",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler iniciado.")