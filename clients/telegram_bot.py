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
from services.user_service import UserService


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


#Método que se llama cuando el usuario quiere registrarse.
#Not implemented yet. Se deberá implementar la lógica de registro de usuarios.
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

async def register_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    name = update.message.text.strip()

    # ¿Ya existe?
    user = UserService.find_user_by_telegram_id(
        telegram_id
    )

    if user is not None:
        #El usuario ya está registrado en telegram
        await update.message.reply_text(
            "Ya existe una solicitud de registro asociada a esta cuenta."
        )

        return ConversationHandler.END

    # Registrar usuario
    UserService.add_user(
        name=name,
        telegram_user_id=telegram_id
    )

    await update.message.reply_text(
        f"Gracias {name}.\n\n"
        "Espera a que el administrador apruebe tu registro. Te avisaré cuando esté listo."
    )

    return ConversationHandler.END


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

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help_command))

    app.add_handler(register_handler)

    #Handler que llama al método echo cuando el usuario envía un mensaje de texto que no es un comando.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,echo))

    print("MarIA está ejecutándose...")
    app.run_polling() #arranca el bot y lo pone a escuchar mensajes de Telegram mediante Polling. Deberá cambiarse a Webhooks en producción.


#
# Punto de entrada al Telegram Bot.
if __name__ == "__main__":
    main()