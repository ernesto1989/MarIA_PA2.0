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
    MessageHandler,
    ContextTypes,
    filters
)

from agent.assistant import MariaAssistant


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") #el token para comunicarse con telegram. Se obtiene de BotFather en Telegram.
assistant = MariaAssistant() #El agente MarIA.


#Método que se llama cuando el usuario envía el comando /start. Se le da la bienvenida al usuario.
async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "¡Hola! Soy MarIA 👋"
    )

#Método que se llama cuando el usuario quiere registrarse.
#Not implemented yet. Se deberá implementar la lógica de registro de usuarios.
async def register(update: Update,
                   context: ContextTypes.DEFAULT_TYPE):
    pass

#Método que se llama cuando el usuario quiere solicitar ayuda al bot.
async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE):
    pass


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

    #Comando /start
    #supongo que algo similar deberá hacerse para /register y /help, pero no lo implementé todavía.
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    #Handler que llama al método echo cuando el usuario envía un mensaje de texto que no es un comando.
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo
        )
    )

    print("MarIA está ejecutándose...")
    app.run_polling() #arranca el bot y lo pone a escuchar mensajes de Telegram mediante Polling. Deberá cambiarse a Webhooks en producción.


#
# Punto de entrada al Telegram Bot.
if __name__ == "__main__":
    main()