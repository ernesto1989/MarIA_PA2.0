# MarIA 🤖

MarIA (My Artificial Intelligent Assistant) es un asistente personal desarrollado en Python que utiliza OpenAI Agents SDK y Telegram para administrar tareas, recordatorios y actividades personales mediante lenguaje natural.

Actualmente funciona como un asistente conversacional capaz de crear, consultar y administrar tareas, además de generar recordatorios inteligentes programados mediante un scheduler.

---

# Características

## Gestión de tareas

- Crear tareas mediante lenguaje natural.
- Consultar tareas pendientes.
- Consultar una tarea específica.
- Actualizar tareas.
- Marcar tareas como completadas.
- Limpieza automática de tareas terminadas.

## Recordatorios

MarIA soporta tres tipos de recordatorios:

### Task Reminder

Recordatorios asociados a una tarea existente.

Ejemplo:

> Recuérdame 15 minutos antes de la reunión.

---

### One Shot Reminder

Recordatorios independientes que se ejecutan una sola vez.

Ejemplo:

> Recuérdame mañana a las 7 pm llamar al banco.

---

### Recurring Reminder

Recordatorios recurrentes.

Actualmente soporta:

- Diario
- Semanal
- Mensual
- Anual

Ejemplos:

> Todos los lunes a las 8 am.

> Todos los días a las 9 pm.

> Cada día 15 de mes.

> Todos los 29 de febrero.

---

# Arquitectura

```
Telegram
      │
      ▼
Telegram Bot
      │
      ▼
MarIA Assistant (OpenAI Agents SDK)
      │
      ├────────────── Tools
      │                   │
      ▼                   ▼
 Activity Service     Reminder Service
      │                   │
      └──────────────┬────┘
                     ▼
                 MySQL Database
```

---

# Scheduler

MarIA utiliza APScheduler para ejecutar tareas automáticas.

Jobs actuales:

- Recordatorio diario de tareas.
- Recordatorio semanal.
- Recordatorio mensual.
- Limpieza automática de tareas terminadas.
- Procesamiento de recordatorios cada minuto.

Para ejecutar código asíncrono desde `BackgroundScheduler` se utiliza un `AsyncRunner` dedicado que mantiene un único Event Loop reutilizable.

---

# Base de datos

Actualmente el sistema administra las siguientes entidades principales:

- Users
- Activities (Tasks)
- Reminders
- Reminder Weekdays

---

# Tecnologías

- Python 3.13
- OpenAI Agents SDK
- python-telegram-bot
- APScheduler
- MySQL
- httpx
- asyncio

---

# Estructura del proyecto

```
agent/
clients/
database/
notifications/
scheduler/
services/
utils/
```

---

# Funcionalidades implementadas

## Usuarios

- Registro
- Activación
- Consulta

## Tareas

- Crear
- Consultar
- Actualizar
- Completar
- Limpieza automática

## Recordatorios

- Crear recordatorios de tarea
- Crear recordatorios únicos
- Crear recordatorios recurrentes
- Procesamiento automático
- Notificaciones por Telegram

---

# Roadmap

## Corto plazo

- Documentación técnica completa.
- Actualizar recordatorios.
- Eliminar recordatorios.
- Deshabilitar/Habilitar recordatorios.

## Mediano plazo

- Listas y Checklists.
- Progreso de tareas.
- Continuidad conversacional mejorada.

## Largo plazo

- Administración de proyectos.
- Integración con WhatsApp.
- Gestión multiusuario.
- Compartición de tareas.
- Panel Web.

---

# Estado del proyecto

Actualmente MarIA se encuentra en una fase funcional de pruebas.

Los módulos de tareas y recordatorios están siendo validados antes de continuar con nuevas funcionalidades.