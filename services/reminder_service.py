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
from services.activity_service import ActivityService
from utils.logger import logger

from notifications.notifier import (
    notify_daily_tasks,
    notify_week_tasks,
    notify_month_tasks,
    notify_clean_tasks
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

                tasks = ActivityService.find_tasks_for_today(
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

                tasks = ActivityService.find_tasks_for_this_week(
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

                tasks = ActivityService.find_tasks_for_this_month(
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
            ActivityService.cleanup_completed_tasks()
            await notify_clean_tasks()
        except Exception:
            logger.exception("Error ejecutando limpieza de tareas completadas")
            raise

            