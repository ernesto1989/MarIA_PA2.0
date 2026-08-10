"""
Archivo speech_service.py

Aquí se maneja la interpretación de mensajes de voz (en español).
Se regresa un texto para que el agente lo interprete
"""

import whisper
import os
from dotenv import load_dotenv

_model = whisper.load_model("small")
load_dotenv()
TEMP_FILE = 'C:/Conciencia/temp_files/'#os.getenv("TEMP_FILE")

class SpeechService:

    @staticmethod
    async def process_voicemsg(update):
        try:
            voice_file = await update.message.voice.get_file()
            temp_filename = f"{TEMP_FILE}voz_{update.message.message_id}.ogg"
            await voice_file.download_to_drive(temp_filename)
            text = await SpeechService.transcribe(temp_filename)
            return text
        except Exception as e:
            await update.message.reply_text(f"Ocurrió un error al procesar el audio: {str(e)}")
        finally:
            # 7. Limpieza: Borramos el archivo temporal del disco para no llenar el servidor
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


    @staticmethod
    async def transcribe(temp_filename) -> str:
        result = _model.transcribe(temp_filename,language="spanish")
        translated_text = result.get("text", "").strip()

        return translated_text