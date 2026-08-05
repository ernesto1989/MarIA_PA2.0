"""
reminder_service.py

Contiene la lógica de negocio relacionada con
recordatorios automáticos de MarIA.
"""

from services.user_service import UserService
from services.activity_service import ActivityService

from notifications.notifier import (
    notify_daily_tasks,
    notify_week_tasks,
    notify_month_tasks,
    notify_clean_tasks
)


class ReminderService:

    @staticmethod
    async def daily_tasks():

        # Obtener todos los usuarios activos
        users = UserService.find_active_users()

        for user in users:

            tasks = ActivityService.find_tasks_for_today(
                user["id"]
            )

            if not tasks:
                continue

            await notify_daily_tasks(
                user,
                tasks
            )

    @staticmethod
    async def week_tasks():

        # Obtener todos los usuarios activos
        users = UserService.find_active_users()

        for user in users:

            tasks = ActivityService.find_tasks_for_this_week(
                user["id"]
            )

            if not tasks:
                continue

            await notify_week_tasks(
                user,
                tasks
            )

    @staticmethod
    async def month_tasks():

        # Obtener todos los usuarios activos
        users = UserService.find_active_users()

        for user in users:

            tasks = ActivityService.find_tasks_for_this_month(
                user["id"]
            )

            if not tasks:
                continue

            await notify_month_tasks(
                user,
                tasks
            )

    @staticmethod
    async def clean_tasks():

        ActivityService.cleanup_completed_tasks()
        await notify_clean_tasks()

            