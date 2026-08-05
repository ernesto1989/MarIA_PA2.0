'''
notifier.py

Procesa todo el envío de mensajes al usuario para ciertos aspectos importantes.

1.Notifica al admin de un nuevo usuario y al usuario si fue o no aprovado
2.Notifica los pendientes del día
3.Notifica los pendientes de la semana
4.Notifica los pendientes del mes.
5.Notifica al admin del borrado de actividades. 
'''
from clients import telegram_client

from .templates import (
    NEW_USER_TEMPLATE,
    USER_APPROVED_TEMPLATE,
    USER_DENIED_TEMPLATE
)

from services.user_service import UserService

#Notifica al admin del registro
async def notify_admin_new_user(
    admin,
    user
):

    message = NEW_USER_TEMPLATE.format(
        name=user["name"],
        user_id=user["id"],
        telegram_id=user["telegram_user_id"]
    )

    await telegram_client.send_message(
        admin["telegram_user_id"],
        message
    )

#notifica si el usuario fue aprobado
async def notify_user_approved(user):

    await telegram_client.send_message(
        user["telegram_user_id"],
        USER_APPROVED_TEMPLATE
    )

#notifica si el usuario fue rechazado
async def notify_user_denied(user):

    await telegram_client.send_message(
        user["telegram_user_id"],
        USER_DENIED_TEMPLATE
    )

## Estos notifications no tienen tamplate porque se crean al vuelo.

#Notificación de tareas diarias
async def notify_daily_tasks(
    user,
    tasks
):

    message = "📅 Buenos días.\n\n"

    message += "Estas son tus actividades para hoy:\n\n"

    for index, task in enumerate(tasks, start=1):

        message += (
            f"{index}. {task['title']}\n"
            f"   Prioridad: {task['priority']}\n"
            f"   Vence: {task['due_date']}\n\n"
        )

    await telegram_client.send_message(
        user["telegram_user_id"],
        message
    )

#Notificación de tareas semanales
async def notify_week_tasks(
    user,
    tasks
):

    message = "📅 Buenos días.\n\n"

    message += "Estas son tus actividades para la semana:\n\n"

    for index, task in enumerate(tasks, start=1):

        message += (
            f"{index}. {task['title']}\n"
            f"   Prioridad: {task['priority']}\n"
            f"   Vence: {task['due_date']}\n\n"
        )

    await telegram_client.send_message(
        user["telegram_user_id"],
        message
    )

#Notificación de tareas mensuales
async def notify_month_tasks(
    user,
    tasks
):

    message = "📅 Buenos días.\n\n"

    message += "Estas es tu mes:\n\n"

    for index, task in enumerate(tasks, start=1):

        message += (
            f"{index}. {task['title']}\n"
            f"   Prioridad: {task['priority']}\n"
            f"   Vence: {task['due_date']}\n\n"
        )

    await telegram_client.send_message(
        user["telegram_user_id"],
        message
    )

#Notificación de borrado de tareas
async def notify_clean_tasks():

    message = "Borrado de actividades terminadas ejecutado. Gracias por confiar en MarIA."

    user = UserService.find_admin()

    await telegram_client.send_message(
        user["id"], 
        message
    )