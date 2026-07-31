# MarIA

MarIA (My Artificial Research Intelligent Assistant) es un asistente personal basado en IA orientado inicialmente a la gestión de actividades del doctorado y tareas personales mediante Telegram.

## Objetivos

- Gestión de actividades.
- Interacción mediante lenguaje natural.
- Recordatorios automáticos.
- Automatización de tareas.
- Integración futura con Gmail, Google Calendar y Google Drive.

---

## Tecnologías

- Python
- Telegram Bot API
- MySQL
- OpenAI Agents
- APScheduler (próximamente)

---

## Estructura del proyecto

```
MARIA/

├── bot/
├── database/
├── services/
├── .env
├── requirements.txt
└── README.md
```

---

## Instalación

Crear ambiente virtual

```bash
python -m venv .venv
```

Activar

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Variables de entorno

Crear un archivo `.env`

```text
BOT_TOKEN=

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

## Estado del proyecto

### MVP

- [x] Bot Telegram
- [x] Base de datos
- [x] Servicios
- [ ] Agente IA
- [ ] Scheduler
- [ ] Despliegue
- [ ] Registro de usuarios