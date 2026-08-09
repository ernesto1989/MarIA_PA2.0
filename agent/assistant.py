'''
Bot de MarIA. 

Archivo que crea el agente y lo conecta con el LLM.
Es importante mencionar que el LLM genera solo el procesamiento de lenguaje natural.
El agente contiene los tools necesarios para realizar las acciones a las cuales se le programó.

'''
import os
from dotenv import load_dotenv
from agents import Agent
from agents import Runner
from services.user_service import UserService
from .instructions import SYSTEM_PROMPT
from .tools import build_find_tasks_tool,build_find_task_tool,build_add_task_tool,build_update_task_tool,build_cleanup_completed_tasks_tool,build_add_task_reminder_tool,build_add_one_shot_reminder_tool,build_add_recurring_reminder_tool
from services.conversation_service import ConversationService


load_dotenv()

#Cada usuario tendrá su propio agente MarIA, con su propio contexto y herramientas. 
# Por eso se crea la clase MariaAssistant, que es la que se encarga de crear el agente MarIA para cada usuario.
class MariaAssistant:

    async def process_message(
        self,
        telegram_user_id,
        message
    ):

        # Buscar al usuario por su Telegram ID
        user = UserService.find_user_by_telegram_id(
            telegram_user_id
        )

        # Usuario no registrado
        if user is None:
            return (
                "No estás registrado.\n"
                "Solicita tu registro con /register."
            )

        # Usuario pendiente o deshabilitado
        if user["status"] != "ACTIVE":
            return (
                "Tu cuenta aún no ha sido activada."
            )

        ConversationService.add_user_message(
            telegram_user_id,
            message
        )

        history = ConversationService.get_history(
            telegram_user_id
        )

        # Construir el agente para este usuario
        agent = Agent(
            name="MarIA",
            instructions=SYSTEM_PROMPT,
            model=os.getenv("MODEL"),
            tools=[
                build_find_tasks_tool(user["id"]),
                build_find_task_tool(user["id"]),
                build_add_task_tool(user["id"]),
                build_update_task_tool(user["id"]),
                build_cleanup_completed_tasks_tool(user["id"]),
                build_add_task_reminder_tool(user["id"]),
                build_add_one_shot_reminder_tool(user["id"]),
                build_add_recurring_reminder_tool(user["id"])
            ]
        )

        # Agregar contexto del usuario al prompt
        conversation = ""

        for msg in history:

            conversation += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        prompt = f"""
        Información del usuario

        Nombre: {user['name']}

        Historial de conversación:

        {conversation}

        Responde únicamente al último mensaje del usuario teniendo en cuenta el contexto anterior.
        """

        # Ejecutar el agente
        result = await Runner.run(
            agent,
            prompt
        )

        ConversationService.add_assistant_message(
            telegram_user_id,
            result.final_output
        )

        return result.final_output