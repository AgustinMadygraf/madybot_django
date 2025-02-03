"""
Path: app/infrastructure/database_connection.py
Módulo de conexión a MySQL utilizando SQLAlchemy.
"""

from app.core.config import db
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class DatabaseConnection:
    """
    Clase que maneja la sesión de la base de datos utilizando SQLAlchemy.
    """

    @staticmethod
    def get_session():
        """
        Retorna la sesión activa de la base de datos.
        """
        return db.session

    @staticmethod
    def close_session():
        """
        Cierra la sesión activa de la base de datos.
        """
        try:
            db.session.close()
            logger.info("Sesión de base de datos cerrada correctamente.")
        except Exception as e:
            logger.error("Error al cerrar la sesión de base de datos: %s", e)
