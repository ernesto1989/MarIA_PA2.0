import logging
import os

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/maria.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MarIA")