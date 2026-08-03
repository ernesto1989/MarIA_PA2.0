###
# Este archivo contiene herramientas para interactuar con las actividades del usuario.
# Crea funciones que le dan funciones al agente.
###
from agents import function_tool
from services.activity_service import ActivityService


def build_find_tasks_tool(user_id):

    @function_tool
    def find_tasks():
        """
        Obtiene todas las actividades del usuario.
        """

        tasks = ActivityService.find_tasks(user_id)

        return tasks

    return find_tasks

def build_find_task_tool(user_id):

    @function_tool
    def find_task(task_id: int):
        """
        Obtiene una actividad específica del usuario mediante su ID.
        Utilízala cuando el usuario haga referencia a una actividad concreta.
        """

        task = ActivityService.find_task(task_id)

        if task is None:
            return "Actividad no encontrada."

        if task["user_id"] != user_id:
            return "La actividad no pertenece al usuario."

        return task

    return find_task

def build_add_task_tool(user_id):

    @function_tool
    def add_task(
        title: str,
        due_date: str,
        priority: str
    ):
        """
        Crea una nueva actividad.

        priority debe ser:
        LOW
        MEDIUM
        URGENT
        """

        task_id = ActivityService.add_task(
            user_id,
            title,
            due_date,
            priority
        )

        return f"Actividad creada correctamente. Id={task_id}"
    
    return add_task


def build_update_task_tool(user_id):

    @function_tool
    def update_task(
        task_id: int,
        title: str = None,
        due_date: str = None,
        priority: str = None,
        status: str = None
    ):
        """
        Actualiza una actividad existente.
        """

        task = ActivityService.find_task(task_id)

        if task is None:
            return "Actividad no encontrada."

        if task["user_id"] != user_id:
            return "La actividad no pertenece al usuario."

        updated = ActivityService.update_task(
            task_id,
            title,
            due_date,
            priority,
            status
        )

        return "Actividad actualizada." if updated else "No hubo cambios."

    return update_task


def build_cleanup_completed_tasks_tool(user_id):

    @function_tool
    def cleanup_completed_tasks():
        """
        Elimina todas las actividades terminadas del usuario.
        """

        ActivityService.cleanup_completed_tasks(
            user_id
        )

        return "Las actividades terminadas fueron eliminadas."

    return cleanup_completed_tasks