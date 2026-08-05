#A diferencia del telegram bot que responde mensajes enviados por el usuario,
#el telegram cliente envía mensajes desde el backend al usuario.

from telegram import Bot

#Clase que concentra el envío de mensajes desde el backend al usuario de Telegram.
class TelegramClient:
    def __init__(self, token):
        self.bot = Bot(token)

    #Método que envía un mensaje a un usuario de Telegram dado su id de Telegram.
    async def send_message(
        self,
        telegram_user_id: int,
        message: str
    ):

        await self.bot.send_message(
            chat_id=telegram_user_id,
            text=message
        )