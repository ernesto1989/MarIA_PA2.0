'''
connection.py

Módulo de conexión a base de datos
Lee de variables de entorno lo necesario para conectarse a la base de datos.
'''
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

#Variables de entorno necesarias para la conexión a la base de datos. Se obtienen del archivo .env.
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

#Método que genera la conexión a la base de datos.
def get_connection():
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )