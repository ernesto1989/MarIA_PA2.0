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