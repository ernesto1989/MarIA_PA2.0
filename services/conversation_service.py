'''
    Script que permite mantener el historial de conversaciones con el usuario.
    Ayuda a mantener el contexto.

    Hay que tener cuidado ya que genera muchos tokens de subida.
'''
from collections import defaultdict


class ConversationService:

    MAX_MESSAGES = 10

    _history = defaultdict(list)

    #Método que busca la historia de conversación de un usuario.
    @classmethod
    def get_history(
        cls,
        telegram_user_id: int
    ):
        return cls._history[telegram_user_id]

    #Método que agrega un mensaje proveniente del usuario
    @classmethod
    def add_user_message(
        cls,
        telegram_user_id: int,
        message: str
    ):
        cls._history[telegram_user_id].append({
            "role": "user",
            "content": message
        })
        cls._trim(
            telegram_user_id
        )

    #Método que agrega un mensaje proveniente del agente
    @classmethod
    def add_assistant_message(
        cls,
        telegram_user_id: int,
        message: str
    ):
        cls._history[telegram_user_id].append({
            "role": "assistant",
            "content": message
        })
        cls._trim(
            telegram_user_id
        )

    #Método que borra el historial de mensajes
    @classmethod
    def clear_history(
        cls,
        telegram_user_id: int
    ):
        cls._history[telegram_user_id] = []

    #Método que determina el total de historial
    @classmethod
    def _trim(
        cls,
        telegram_user_id: int
    ):
        #si el número de mensajes del usuario es mayor al total de mensajes
        if len(cls._history[telegram_user_id]) > cls.MAX_MESSAGES:
            #se elimina el mensaje más viejo
            cls._history[telegram_user_id] = \
                cls._history[telegram_user_id][-cls.MAX_MESSAGES:]