"""
Telegram Bot para MarIA.

Este es el punto de entrada desde el APP de Telegram. El bot se conecta a Telegram, escucha los mensajes de los usuarios y 
los redirecciona al agente MarIA. Espera una respuesta y la envía de vuelta al usuario.

Responsabilidades:

1. Conectarse a Telegram.
2. Escuchar mensajes mediante Polling.
3. Enviar cada mensaje al asistente (MarIA).
4. Regresar la respuesta al usuario.

"""

import os

from dotenv import load_dotenv
from utils.logger import logger

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from agent.assistant import MariaAssistant
from notifications.notifier import notify_admin_new_user,notify_user_approved,notify_user_denied
from services.user_service import UserService
from clients import telegram_client
from scheduler.scheduler import start_scheduler



load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") #el token para comunicarse con telegram. Se obtiene de BotFather en Telegram.
assistant = MariaAssistant() #El agente MarIA.

# Estados del registro
ASK_NAME = 1

#Método que se llama cuando el usuario envía el comando /start. Se le da la bienvenida al usuario.
async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "¡Hola! Soy MarIA - Asistente virtual 👋"
    )

#Método que se llama cuando el usuario quiere solicitar ayuda al bot.
#Método que se llama cuando el usuario quiere solicitar ayuda al bot.
async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE):
    help_text = """
        🤖 *MarIA*

        Asistente personal para la gestión de actividades.

        *Comandos disponibles*

        /help
        Muestra esta ayuda.

        /register
        Solicita el registro para utilizar MarIA.

        *Actualmente puedo:*

        • Consultar tus actividades.
        • Responder preguntas sobre tus pendientes.

        *Próximamente:*

        • Crear actividades.
        • Actualizar actividades.
        • Marcar actividades como terminadas.
        • Recordatorios automáticos.
        • Resúmenes semanales.
        """
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown"
    )


#Método que se llama cuando el usuario quiere registrarse.
#Solo solicita el nombre del usuario.
async def register(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "¡Bienvenido!\n\n"
        "Para registrarte necesito tu nombre completo.\n\n"
        "¿Cómo quieres que te llame?"
    )

    return ASK_NAME

#Método que se llama cuando el usuario envía su nombre para registrarse.
#Se verifica si el usuario ya existe, si no existe se registra y se notifica al administrador.
#Se responde con un mensaje de recepción de solicitud al usuario.
#Hace equipo con el método register.
async def register_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    name = update.message.text.strip()

    # Verificar si el usuario ya existe
    user = UserService.find_user_by_telegram_id(
        telegram_id
    )

    if user is not None:

        if user["status"] == "ACTIVE":

            await update.message.reply_text(
                "Ya estás registrado y tu cuenta se encuentra activa."
            )

        elif user["status"] == "PENDING":

            await update.message.reply_text(
                "Ya existe una solicitud de registro pendiente de aprobación."
            )

        else:

            await update.message.reply_text(
                "Tu cuenta se encuentra deshabilitada. Contacta al administrador."
            )

        return ConversationHandler.END

    try:

        # Registrar usuario
        UserService.add_user(
            name=name,
            telegram_user_id=telegram_id
        )

        # Recuperar el usuario recién creado
        user = UserService.find_user_by_telegram_id(
            telegram_id
        )

        # Buscar administrador
        admin = UserService.find_admin()

        # Notificar al administrador
        await notify_admin_new_user(
            admin,
            user
        )

        # Confirmar al usuario
        await update.message.reply_text(
            "✅ Tu solicitud fue registrada correctamente.\n\n"
            "El administrador ha sido notificado y recibirá una solicitud para aprobar tu acceso.\n\n"
            "Recibirás una notificación cuando tu cuenta sea aprobada."
        )

    except Exception as ex:

        print(ex)

        await update.message.reply_text(
            "❌ Ocurrió un error al registrar tu solicitud.\n"
            "Inténtalo nuevamente más tarde."
        )

    return ConversationHandler.END




#Método utilizado solo para el admin. El objetivo es que cuando el admin
#recibe una solicitud de registro, autoriza o no al usuario. 
#Si lo autoriza, se le notifica al usuario que su cuenta fue aprobada.
async def approve(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    admin = UserService.find_user_by_telegram_id(
        update.effective_user.id
    )

    if admin is None or admin["role"] != "ADMIN":

        await update.message.reply_text(
            "No tienes permisos para ejecutar este comando."
        )

        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Solo puedes autorizar 1 usuario a la vez.\nUso: /approve <user_id>"
        )

        return

    try:

        user_id = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "El id del usuario no es válido."
        )

        return

    user = UserService.find_user_by_id(
        user_id
    )

    if user is None:

        await update.message.reply_text(
            "Usuario no encontrado."
        )

        return

    UserService.update_user(
        user_id=user_id,
        status="ACTIVE"
    )

    user = UserService.find_user_by_id(
        user_id
    )

    await notify_user_approved(
        user
    )

    await update.message.reply_text(
        f"✅ Usuario {user['name']} aprobado correctamente."
    )

#Método que rechaza la petición de registro de un usuario. Solo puede ser ejecutado por el admin.
async def deny(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    admin = UserService.find_user_by_telegram_id(
        update.effective_user.id
    )

    if admin is None or admin["role"] != "ADMIN":

        await update.message.reply_text(
            "No tienes permisos para ejecutar este comando."
        )

        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Uso: /deny <user_id>"
        )

        return

    try:

        user_id = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "El id del usuario no es válido."
        )

        return

    user = UserService.find_user_by_id(
        user_id
    )

    if user is None:

        await update.message.reply_text(
            "Usuario no encontrado."
        )

        return

    UserService.update_user(
        user_id=user_id,
        status="DISABLED"
    )

    user = UserService.find_user_by_id(
        user_id
    )

    await notify_user_denied(
        user
    )

    await update.message.reply_text(
        f"❌ Usuario {user['name']} rechazado."
    )


#Método responsable de procesar los mensajes del usuario.
#
#Primero obtiene el id telegram del usuario y el mensaje que envió.
#Envía el mensaje al agente y espera la respuesta ara enviarla de vuelta al usuario.
async def echo(update: Update,
               context: ContextTypes.DEFAULT_TYPE):

    telegram_user_id = update.effective_user.id
    message = update.message.text

    #Aquí, despues de tener el id de usuario de Telegram y el mensaje, se llama al asistente para procesar la respuesta.
    response = await assistant.process_message(
        telegram_user_id,
        message
    )

    #Aquí envía la respuesta de vuelta a Telegram.
    await update.message.reply_text(
        response
    )

register_handler = ConversationHandler(

    entry_points=[
        CommandHandler(
            "register",
            register
        )
    ],

    states={

        ASK_NAME: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                register_name
            )

        ]

    },

    fallbacks=[]
)

#Log de errores
async def error_handler(update, context):

    logger.exception(
        "Unhandled exception",
        exc_info=context.error
    )


# --------------------------------------------------
# Función principal
#
# Registra todos los handlers y
# pone el bot a escuchar mediante Polling. Pooling es jalar los mensajes de Telegram cada cierto tiempo.
# En Productivo, deberá cambiarse de Polling a Webhooks.
# --------------------------------------------------
def main():

    #Aquí se crea un app con el token del bot, y se registran los handlers de comandos y mensajes.
    app = Application.builder().token(TOKEN).build()

    logger.info("Agregando handlers...")

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help_command))
    app.add_handler(CommandHandler("approve",approve))
    app.add_handler(CommandHandler("deny",deny))
    app.add_handler(register_handler)
    #Handler que llama al método echo cuando el usuario envía un mensaje de texto que no es un comando.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,echo))
    app.add_error_handler(error_handler)

    logger.info("Arrancando scheduler...")
    start_scheduler()

    logger.info("Arrancando agente MarIA + su cliente Telegram")
    app.run_polling() #arranca el bot y lo pone a escuchar mensajes de Telegram mediante Polling. Deberá cambiarse a Webhooks en producción.
    
#
# Punto de entrada al Telegram Bot.
if __name__ == "__main__":
    main()