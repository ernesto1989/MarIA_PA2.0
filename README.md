# MarIA

**MarIA** es un asistente personal basado en Inteligencia Artificial diseñado para ayudar en la gestión de actividades del doctorado y tareas personales mediante lenguaje natural.

Actualmente utiliza Telegram como cliente de comunicación y OpenAI Agents como motor de razonamiento.

---

# Objetivos

- Gestionar actividades personales, familiares y del doctorado.
- Interactuar mediante lenguaje natural.
- Automatizar recordatorios y tareas repetitivas.

---

# Arquitectura

```
                    +----------------------+
                    |      Telegram        |
                    +----------+-----------+
                               |
                               v
                 clients/telegram_bot.py
                               |
                               v
                  agent/MariaAssistant
                               |
                               v
                    OpenAI Agent (GPT)
                               |
                  +------------+------------+
                  |                         |
                  v                         v
             Agent Tools              System Prompt
                  |
                  v
              Services
                  |
                  v
             MySQL Database
```

---

# Estructura del proyecto

```
MARIA/

├── agent/
│   ├── assistant.py
│   ├── instructions.py
│   ├── tools.py
│   └── __init__.py
│
├── clients/
│   ├── telegram_bot.py
│   └── __init__.py
│
├── database/
│   ├── connection.py
│   ├── ddl.sql
│   └── __init__.py
│
├── services/
│   ├── activity_service.py
│   ├── user_service.py
│   └── __init__.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Base de datos

Actualmente el sistema utiliza dos tablas principales.

## users

Información de los usuarios registrados.

- id
- telegram_user_id
- name
- role
- status
- created_at
- updated_at

## activities

Actividades asociadas a cada usuario.

- id
- user_id
- title
- due_date
- priority
- status
- created_at
- updated_at

Además existe el procedimiento almacenado:

```
sp_cleanup_completed_tasks()
```

---

# Servicios implementados

## UserService

- find_user_by_id()
- find_user_by_telegram()
- find_admin()
- add_user()
- update_user()

---

## ActivityService

- find_task()
- find_tasks()
- add_task()
- update_task()
- cleanup_completed_tasks()

---

# Agente

El agente utiliza el SDK oficial de OpenAI Agents.

Actualmente dispone de las siguientes herramientas:

- find_tasks()

El agente selecciona automáticamente la herramienta adecuada según la intención del usuario.

---

# Cliente Telegram

Actualmente el sistema dispone de un cliente Telegram encargado únicamente de:

- recibir mensajes
- delegar el procesamiento al agente
- enviar la respuesta al usuario

Toda la lógica de negocio vive fuera del cliente.

---

# Variables de entorno

```
BOT_TOKEN=

OPENAI_API_KEY=
MODEL=gpt-5-mini

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

# Instalación

Crear el entorno virtual

```bash
python -m venv .maria_venv
```

Activar

Windows

```bash
.maria_venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
python -m clients.telegram_bot
```

---

# Estado del proyecto

## MVP v0.1

### Infraestructura

- [x] Arquitectura del proyecto
- [x] Integración con Telegram
- [x] Integración con OpenAI Agents
- [x] Conexión MySQL
- [x] Servicios
- [x] Primera Tool (find_tasks)

### Pendiente

- [ ] Registro de usuarios
- [ ] Aprobación por administrador
- [ ] Scheduler
- [ ] Recordatorios automáticos
- [ ] CRUD completo mediante herramientas
- [ ] Memoria conversacional

---

# Roadmap

## v0.2

- Registro de usuarios
- Activación por administrador
- Scheduler
- Recordatorios

## v0.3

- CRUD completo de actividades mediante herramientas
- Limpieza automática de tareas terminadas

## v0.4

- Integración con Gmail
- Integración con Google Calendar
- Integración con Google Drive

## Futuro

- Cliente WhatsApp
- Cliente Web
- Memoria persistente
- Múltiples agentes especializados
- Dashboard administrativo

---

# Principios de diseño

- El cliente (Telegram, Web, WhatsApp) nunca contiene lógica de negocio.
- El agente únicamente razona y selecciona herramientas.
- Las herramientas utilizan los servicios.
- Los servicios encapsulan el acceso a la base de datos.
- El sistema está preparado para incorporar nuevos clientes sin modificar el núcleo de MarIA.