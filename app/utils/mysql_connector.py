"""
Path: app/utils/mysql_connector.py
Este script se encarga de manejar la conexión a la base de datos MySQL.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar el logger
logger = LoggerConfigurator().configure()

# Cargar variables de entorno desde el .env
load_dotenv()

class MySQLConnector:
    "Maneja la conexión a la base de datos MySQL."
    def __init__(self):
        self.connection = None
        self.db_name = os.getenv('MYSQL_DATABASE', 'coopebot')  # Nombre de la BD

        try:
            logger.info("Intentando conectar a la base de datos '%s'...", self.db_name)
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=self.db_name
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logger.info("Conectado a MySQL Server versión %s", db_info)
        except Error as e:
            if e.errno == 1049:  # Error 1049: Unknown database
                logger.warning("La base de datos '%s' no existe. Creándola...", self.db_name)
                self._create_database()
                self._reconnect()  # Volver a inicializar la conexión después de crear la BD
            else:
                logger.error("Error al conectar con MySQL: %s", e)

    def _reconnect(self):
        "Reconecta a la base de datos después de crearla."
        try:
            logger.info("Intentando reconectar a la base de datos '%s'...", self.db_name)
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=self.db_name
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logger.info("Re-conectado a MySQL Server versión %s", db_info)
        except Error as e:
            logger.error("Error al reconectar a MySQL: %s", e)

    def _create_database(self):
        """
        Crea la base de datos si no existe.
        """
        try:
            temp_connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', '')
            )
            temp_cursor = temp_connection.cursor()
            temp_cursor.execute(f"CREATE DATABASE {self.db_name}")
            logger.info("Base de datos '%s' creada exitosamente.", self.db_name)
            temp_cursor.close()
            temp_connection.close()
        except Error as e:
            logger.error("Error al crear la base de datos '%s': %s", self.db_name, e)

    def execute_query(self, query, params=None):
        "Ejecuta una consulta en la base de datos."
        if self.connection is None or not self.connection.is_connected():
            logger.warning("No hay conexión con MySQL al intentar ejecutar la consulta.")
            return None
        cursor = self.connection.cursor()
        try:
            logger.debug("Ejecutando consulta: %s con parámetros %s", query, params)
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error("Error ejecutando consulta: %s", e)
            return None

    def fetch_query(self, query, params=None):
        "Obtiene los resultados de una consulta en la base de datos."
        if self.connection is None or not self.connection.is_connected():
            logger.warning("No hay conexión con MySQL al intentar obtener datos.")
            return None
        cursor = self.connection.cursor(dictionary=True)
        try:
            logger.debug("Ejecutando consulta de recuperación: %s con parámetros %s", query, params)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            logger.error("Error obteniendo datos: %s", e)
            return None
