"""
Módulo clients. 

Lugar donde se implementan todos los clientes que se comunicarán con MarIA.

Actualmente se encuentra implementado solo el cliente de Telegram.

Pueden implementarse:

1. Bot/Cliente de whatsapp.
2. Aplicación web.
3. Aplicación móvil.
4. Cliente de escritorio.

Ernesto Cantú
03/08/2026

"""
import os

from dotenv import load_dotenv

from .telegram_client import TelegramClient
load_dotenv()

telegram_client = TelegramClient(os.getenv("BOT_TOKEN")) #El cliente de Telegram que envía mensajes desde el backend al usuario.