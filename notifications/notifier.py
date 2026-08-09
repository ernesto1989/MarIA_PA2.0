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

priority_icons = {
    "URGENT": "🔴 Alta",
    "MEDIUM": "🟡 Media",
    "LOW": "🟢 Baja"
}

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
    pending_tasks,
    completed_tasks
):

    message = "📅 Buenos días.\n\n"

    if pending_tasks:
        message += "Estas son las actividades que tienes programadas para hoy:\n\n"

        for task in sorted(
            pending_tasks,
            key=lambda t: t["priority"],
            reverse=True
        ):

            message += (
                f"• {task['title']}\n"
                f"   {priority_icons[task['priority']]}\n\n"
            )

    if completed_tasks:

        message += "\n✅ Estas actividades tenían como fecha límite hoy y ya las has completado:\n\n"

        for task in sorted(
            completed_tasks,
            key=lambda t: t["priority"],
            reverse=True
        ):

            message += f"• {task['title']}\n"

    if not pending_tasks and not completed_tasks:

        message += (
            "Hoy no tienes actividades programadas/por hacer. Puedes rascarte las verijas o lo que te parezca mejor."
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
            f"    {priority_icons[task['priority']]}\n"
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
        user["telegram_user_id"], 
        message
    )


async def notify_task_reminder(reminder):

    message = (
        "⏰ Recordatorio\n\n"
        f"Tienes programada la siguiente actividad:\n\n"
        f"📌 {reminder['title']}\n"
        f"📅 {reminder['due_date']}\n"
        f"🕒 {reminder['due_time']}"
    )

    await telegram_client.send_message(
        reminder["telegram_user_id"],
        message
    )

async def notify_one_shot_reminder(reminder):

    message = (
        "🔔 Recordatorio\n\n"
        f"{reminder['title']}"
    )

    await telegram_client.send_message(
        reminder["telegram_user_id"],
        message
    )

async def notify_recurring_reminder(reminder):

    message = (
        "🔁 Recordatorio\n\n"
        f"{reminder['title']}"
    )

    await telegram_client.send_message(
        reminder["telegram_user_id"],
        message
    )

