"""
Módulo de conexión a MySQL.
Ubicación: app/infrastructure/database.py
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

# Cargar variables de entorno
load_dotenv()

class DatabaseConnection:
    "Maneja la conexión a MySQL."

    def __init__(self):
        self.connection = None
        self.db_name = os.getenv('MYSQL_DATABASE', 'coopebot')

    def connect(self):
        "Establece conexión con MySQL."
        try:
            logger.info("Intentando conectar a la BD '%s'...", self.db_name)
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=self.db_name
            )
            if self.connection.is_connected():
                logger.info("Conexión exitosa a MySQL.")
        except Error as e:
            if e.errno == 1049:  # Error: BD no existe
                logger.warning("La base de datos '%s' no existe. Creándola...", self.db_name)
                self._create_database()
                self.connect()  # Intentar conectar nuevamente
            else:
                logger.error("Error al conectar con MySQL: %s", e)

    def _create_database(self):
        "Crea la base de datos si no existe."
        try:
            temp_conn = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', '')
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute(f"CREATE DATABASE {self.db_name}")
            logger.info("Base de datos '%s' creada exitosamente.", self.db_name)
            temp_cursor.close()
            temp_conn.close()
        except Error as e:
            logger.error("Error al crear la base de datos '%s': %s", self.db_name, e)

    def get_connection(self):
        "Retorna la conexión activa a MySQL."
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection

    def close_connection(self):
        "Cierra la conexión con MySQL."
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión con MySQL cerrada correctamente.")
