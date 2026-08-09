'''
    Script que permite mantener el historial de conversaciones con el usuario.
    Ayuda a mantener el contexto.

    Hay que tener cuidado ya que genera muchos tokens de subida.
'''
from collections import defaultdict


class ConversationService:

    MAX_MESSAGES = 10

    _history = defaultdict(list)

    @classmethod
    def get_history(
        cls,
        telegram_user_id: int
    ):
        return cls._history[telegram_user_id]

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

    @classmethod
    def clear_history(
        cls,
        telegram_user_id: int
    ):
        cls._history[telegram_user_id] = []

    @classmethod
    def _trim(
        cls,
        telegram_user_id: int
    ):
        if len(cls._history[telegram_user_id]) > cls.MAX_MESSAGES:
            cls._history[telegram_user_id] = \
                cls._history[telegram_user_id][-cls.MAX_MESSAGES:]