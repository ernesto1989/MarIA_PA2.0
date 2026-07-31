from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

# El token permite ubicar al bot de Telegram.
TOKEN = os.getenv("BOT_TOKEN") 

# método llamado cuando se ejecuta el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy MarIA perro 👋"
    )


# método llamado cuando se recibe un mensaje de texto
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    #print(update.effective_user.id)
    #print(update.effective_user.username)
    #print(update.effective_chat.id)
    
    print(update.message.text)

    await update.message.reply_text(
        f"Recibí tu mensaje:\n\n{texto}"
    )


def main():

    app = Application.builder().token(TOKEN).build() # crea la aplicación del bot con el token
    app.add_handler(CommandHandler("start", start)) # agrega el handler cuando se ejecuta el comando /start

    # se agrega el handler para recibir mensajes de texto que no sean comandos
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, #valida que el mensaje sea de texto y no sea un comando
            echo #enlaza con el método echo para responder a los mensajes de texto
        )
    )

    print("MarIA está ejecutándose...")

    app.run_polling() #empieza a jalar mensajes desde telegram y ejecuta los handlers correspondientes


if __name__ == "__main__":
    main()