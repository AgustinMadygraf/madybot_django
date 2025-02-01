"""
Path: app/infrastructure/repository.py
Módulo de ejecución de consultas SQL utilizando SQLAlchemy.
"""

from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database_connection import DatabaseConnection
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class Repository:
    """
    Clase base para manejar operaciones en la base de datos con SQLAlchemy.
    """

    def __init__(self):
        self.session = DatabaseConnection.get_session()

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL que modifica datos (INSERT, UPDATE, DELETE).
        """
        try:
            logger.debug("Ejecutando query: %s con params: %s", query, params)
            result = self.session.execute(query, params)
            self.session.commit()
            return result.lastrowid
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Error ejecutando query: %s", e)
            return None

    def fetch_query(self, query, params=None):
        """
        Ejecuta una consulta SQL que devuelve resultados (SELECT).
        """
        try:
            logger.debug("Ejecutando consulta SELECT: %s con params: %s", query, params)
            result = self.session.execute(query, params)
            return result.fetchall()
        except SQLAlchemyError as e:
            logger.error("Error obteniendo datos: %s", e)
            return None
