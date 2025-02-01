"""
Módulo de gestión de usuarios en la base de datos con SQLAlchemy.
Ubicación: app/repositories/user_repository.py
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from app.infrastructure.database_connection import DatabaseConnection
from app.utils.logging.logger_configurator import LoggerConfigurator
from sqlalchemy.ext.declarative import declarative_base

# Configuración del logger
logger = LoggerConfigurator().configure()

# Base de SQLAlchemy
Base = declarative_base()

class User(Base):
    """
    Modelo SQLAlchemy para la tabla `users`.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, nullable=False)
    user_name = Column(String(255), nullable=True)
    user_email = Column(String(255), nullable=True)

class UserRepository:
    """
    Repositorio de usuarios utilizando SQLAlchemy.
    """

    def __init__(self):
        self.session: Session = DatabaseConnection.get_session()

    def ensure_user_exists(self, user_id, user_name=None, user_email=None):
        """
        Verifica si un usuario existe en la BD y lo inserta si no está.
        """
        try:
            existing_user = self.session.query(User).filter_by(user_id=user_id).first()

            if not existing_user:
                new_user = User(user_id=user_id, user_name=user_name, user_email=user_email)
                self.session.add(new_user)
                self.session.commit()
                logger.info("Usuario %s insertado correctamente.", user_id)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Error en ensure_user_exists: %s", e)
