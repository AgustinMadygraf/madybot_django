# app/repositories/conversation_repository.py

from app.models import Conversation
from app.core.config import db
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class ConversationRepository:
    """
    Repositorio para gestionar la persistencia de conversaciones en la base de datos.
    """

    def save_conversation(self, user_id, message, response=None):
        """
        Guarda una nueva conversación en la base de datos.

        :param user_id: ID del usuario al que pertenece la conversación.
        :param message: Mensaje enviado por el usuario.
        :param response: Respuesta generada (puede ser None si aún no se ha generado).
        :return: Objeto Conversation insertado o None en caso de error.
        """
        try:
            conversation = Conversation(user_id=user_id, message=message, response=response)
            db.session.add(conversation)
            db.session.commit()
            logger.info("Conversación guardada correctamente para el usuario %s", user_id)
            return conversation
        except Exception as e:
            db.session.rollback()
            logger.error("Error al guardar la conversación: %s", e)
            return None

    def get_conversation_by_id(self, conversation_id):
        """
        Obtiene una conversación por su ID.

        :param conversation_id: ID único de la conversación.
        :return: Objeto Conversation si se encuentra, None en caso contrario.
        """
        try:
            conversation = Conversation.query.filter_by(id=conversation_id).first()
            if conversation:
                return conversation
            else:
                logger.warning("No se encontró la conversación con ID %s", conversation_id)
                return None
        except Exception as e:
            logger.error("Error al obtener la conversación %s: %s", conversation_id, e)
            return None

    def get_conversations_by_user(self, user_id, limit=10):
        """
        Obtiene las últimas conversaciones de un usuario.

        :param user_id: ID del usuario.
        :param limit: Cantidad máxima de conversaciones a recuperar (por defecto 10).
        :return: Lista de objetos Conversation.
        """
        try:
            conversations = (
                Conversation.query.filter_by(user_id=user_id)
                .order_by(Conversation.created_at.desc())
                .limit(limit)
                .all()
            )
            return conversations
        except Exception as e:
            logger.error("Error al obtener conversaciones para el usuario %s: %s", user_id, e)
            return []

    def update_conversation_response(self, conversation_id, response):
        """
        Actualiza la respuesta de una conversación ya existente.

        :param conversation_id: ID de la conversación a actualizar.
        :param response: Nueva respuesta generada.
        :return: Objeto Conversation actualizado o None en caso de error.
        """
        try:
            conversation = Conversation.query.filter_by(id=conversation_id).first()
            if conversation:
                conversation.response = response
                db.session.commit()
                logger.info("Respuesta de la conversación %s actualizada correctamente.", conversation_id)
                return conversation
            else:
                logger.warning("No se encontró la conversación con ID %s para actualizar.", conversation_id)
                return None
        except Exception as e:
            db.session.rollback()
            logger.error("Error al actualizar la respuesta de la conversación %s: %s", conversation_id, e)
            return None

    def delete_conversation(self, conversation_id):
        """
        Elimina una conversación de la base de datos.

        :param conversation_id: ID de la conversación a eliminar.
        :return: True si la eliminación fue exitosa, False en caso de error.
        """
        try:
            conversation = Conversation.query.filter_by(id=conversation_id).first()
            if conversation:
                db.session.delete(conversation)
                db.session.commit()
                logger.info("Conversación %s eliminada correctamente.", conversation_id)
                return True
            else:
                logger.warning("No se encontró la conversación con ID %s para eliminar.", conversation_id)
                return False
        except Exception as e:
            db.session.rollback()
            logger.error("Error al eliminar la conversación %s: %s", conversation_id, e)
            return False
