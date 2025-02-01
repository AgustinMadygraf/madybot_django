"""
Módulo de ejecución de consultas SQL.
Ubicación: app/infrastructure/repository.py
"""

from mysql.connector import Error
from app.infrastructure.database import DatabaseConnection
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class Repository:
    "Ejecuta consultas en la base de datos."

    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

    def execute_query(self, query, params=None):
        "Ejecuta una consulta SQL que modifica datos (INSERT, UPDATE, DELETE)."
        cursor = self.connection.cursor()
        try:
            logger.debug("Ejecutando query: %s con params: %s", query, params)
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error("Error ejecutando query: %s", e)
            return None
        finally:
            cursor.close()

    def fetch_query(self, query, params=None):
        "Ejecuta una consulta SQL que devuelve resultados (SELECT)."
        cursor = self.connection.cursor(dictionary=True)
        try:
            logger.debug("Ejecutando consulta SELECT: %s con params: %s", query, params)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            logger.error("Error obteniendo datos: %s", e)
            return None
        finally:
            cursor.close()

    def close(self):
        "Cierra la conexión con la BD."
        self.db.close_connection()
