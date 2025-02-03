"""
Path: app/components/services/data/conversation_persistence_service.py
Servicio para gestionar la persistencia de conversaciones.
Aplica el SRP, usando el patrón de repositorio para comunicarse con la base de datos.
"""

from sqlalchemy.exc import DatabaseError, IntegrityError
from app.repositories.conversation_repository import ConversationRepository
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class ConversationPersistenceService:
    def __init__(self, conversation_repository: ConversationRepository):
        self.conversation_repository = conversation_repository

    def save_conversation(self, conversation_data: dict):
        """
        Guarda una nueva conversación en la base de datos.
        Retorna el ID de la conversación insertada o None en caso de error.
        """
        try:
            user_id = conversation_data.get("user_id")
            message = conversation_data.get("message")
            response = conversation_data.get("response")
            conversation = self.conversation_repository.save_conversation(
                user_id=user_id,
                message=message,
                response=response
            )
            if conversation:
                logger.info("Conversación guardada para el usuario %s", user_id)
                return conversation.id
            return None
        except (KeyError, TypeError, DatabaseError, IntegrityError) as e:
            logger.error("Error al guardar la conversación: %s", e)
            return None

    def update_conversation_response(self, conversation_id, response):
        """
        Actualiza la respuesta de una conversación existente.
        """
        try:
            conversation = self.conversation_repository.update_conversation_response(conversation_id, response)
            if conversation:
                logger.info("Respuesta de la conversación %s actualizada correctamente.", conversation_id)
            return conversation
        except (KeyError, TypeError, DatabaseError, IntegrityError) as e:
            logger.error("Error al actualizar la respuesta de la conversación %s: %s", conversation_id, e)
            return None

    def get_conversations_by_user(self, user_id, limit=10):
        """
        Obtiene las últimas conversaciones de un usuario.
        """
        try:
            return self.conversation_repository.get_conversations_by_user(user_id, limit)
        except (KeyError, TypeError, DatabaseError, IntegrityError) as e:
            logger.error("Error al obtener conversaciones para el usuario %s: %s", user_id, e)
            return []

    def delete_conversation(self, conversation_id):
        """
        Elimina una conversación de la base de datos.
        """
        try:
            success = self.conversation_repository.delete_conversation(conversation_id)
            if success:
                logger.info("Conversación %s eliminada correctamente.", conversation_id)
            return success
        except (KeyError, TypeError, DatabaseError, IntegrityError) as e:
            logger.error("Error al eliminar la conversación %s: %s", conversation_id, e)
            return False
