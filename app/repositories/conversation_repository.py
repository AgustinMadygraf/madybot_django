"""
Path: app/repositories/conversation_repository.py
Módulo de gestión de conversaciones en la base de datos con SQLAlchemy.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from app.infrastructure.database_connection import DatabaseConnection
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.repositories.user_repository import UserRepository
from sqlalchemy.ext.declarative import declarative_base

# Configuración del logger
logger = LoggerConfigurator().configure()

# Base de SQLAlchemy
Base = declarative_base()

class Conversation(Base):
    """
    Modelo SQLAlchemy para la tabla `conversations`.
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

class ConversationRepository:
    """
    Repositorio de conversaciones utilizando SQLAlchemy.
    """

    def __init__(self):
        self.session: Session = DatabaseConnection.get_session()
        self.user_repo = UserRepository()

    def insert_conversation(self, user_id, message, response=None):
        """
        Guarda una conversación en la base de datos.
        """
        try:
            # Asegurar que el usuario existe antes de insertar la conversación
            self.user_repo.ensure_user_exists(user_id)

            conversation = Conversation(
                user_id=user_id,
                message=message,
                response=response
            )

            self.session.add(conversation)
            self.session.commit()
            logger.info("Conversación almacenada correctamente para user_id: %s", user_id)
            return conversation.id
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Error insertando conversación: %s", e)
            return None
