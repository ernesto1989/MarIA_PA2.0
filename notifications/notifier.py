from clients import telegram_client

from .templates import (
    NEW_USER_TEMPLATE,
    USER_APPROVED_TEMPLATE,
    USER_DENIED_TEMPLATE
)


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


async def notify_user_approved(user):

    await telegram_client.send_message(
        user["telegram_user_id"],
        USER_APPROVED_TEMPLATE
    )


async def notify_user_denied(user):

    await telegram_client.send_message(
        user["telegram_user_id"],
        USER_DENIED_TEMPLATE
    )

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