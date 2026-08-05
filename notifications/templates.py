NEW_USER_TEMPLATE = """
🔔 Nuevo usuario registrado

    Nombre: {name}
    
    ID interno: {user_id}

    Telegram ID: {telegram_id}

    Comandos disponibles:

    /approve {user_id}

    /deny {user_id}
"""

USER_APPROVED_TEMPLATE = """
    Tu cuenta ha sido aprobada por el administrador.

    Ya puedes comenzar a utilizar el asistente.
"""


USER_DENIED_TEMPLATE = """
    Tu solicitud para utilizar MarIA fue rechazada.

    Si consideras que se trata de un error, contacta al administrador.
"""