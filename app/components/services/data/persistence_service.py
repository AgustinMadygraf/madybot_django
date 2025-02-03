# app/components/services/data/persistence_service.py

from app.repositories.user_repository import UserRepository
from app.repositories.conversation_repository import ConversationRepository
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class PersistenceService:
    """
    Servicio para gestionar la persistencia de datos en la base de datos.
    Se encarga de operaciones de inserción, actualización y eliminación para usuarios y conversaciones.
    """

    def __init__(self, user_repository: UserRepository, conversation_repository: ConversationRepository):
        self.user_repository = user_repository
        self.conversation_repository = conversation_repository

    def save_user(self, user_data: dict):
        """
        Guarda o actualiza los datos del usuario en la base de datos.

        :param user_data: Diccionario con la información del usuario.
        :return: Objeto User insertado/actualizado o None en caso de error.
        """
        try:
            user_id = user_data.get("id")
            browser_data = user_data.get("browserData", {})

            user = self.user_repository.save_user(
                user_id=user_id,
                userAgent=browser_data.get("userAgent"),
                screenResolution=browser_data.get("screenResolution"),
                language=browser_data.get("language"),
                platform=browser_data.get("platform"),
            )
            if user:
                logger.info("Usuario guardado/actualizado con ID: %s", user_id)
            return user
        except Exception as e:
            logger.error("Error al guardar el usuario: %s", e)
            return None

    def save_conversation(self, conversation_data: dict):
        """
        Guarda una nueva conversación en la base de datos.

        :param conversation_data: Diccionario con los datos de la conversación.
        :return: Objeto Conversation insertado o None en caso de error.
        """
        try:
            user_id = conversation_data.get("user_id")
            message = conversation_data.get("message")
            response = conversation_data.get("response")

            conversation = self.conversation_repository.save_conversation(
                user_id=user_id, message=message, response=response
            )

            if conversation:
                logger.info("Conversación guardada para el usuario %s", user_id)
            return conversation
        except Exception as e:
            logger.error("Error al guardar la conversación: %s", e)
            return None

    def update_conversation_response(self, conversation_id, response):
        """
        Actualiza la respuesta de una conversación en la base de datos.

        :param conversation_id: ID de la conversación a actualizar.
        :param response: Nueva respuesta generada.
        :return: Objeto Conversation actualizado o None en caso de error.
        """
        try:
            conversation = self.conversation_repository.update_conversation_response(conversation_id, response)
            if conversation:
                logger.info("Respuesta de la conversación %s actualizada correctamente.", conversation_id)
            return conversation
        except Exception as e:
            logger.error("Error al actualizar la respuesta de la conversación %s: %s", conversation_id, e)
            return None

    def get_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID.

        :param user_id: ID del usuario.
        :return: Objeto User si se encuentra, None en caso contrario.
        """
        try:
            user = self.user_repository.get_user_by_id(user_id)
            return user
        except Exception as e:
            logger.error("Error al obtener usuario %s: %s", user_id, e)
            return None

    def get_conversations_by_user(self, user_id, limit=10):
        """
        Obtiene las últimas conversaciones de un usuario.

        :param user_id: ID del usuario.
        :param limit: Cantidad máxima de conversaciones a recuperar (por defecto 10).
        :return: Lista de objetos Conversation.
        """
        try:
            conversations = self.conversation_repository.get_conversations_by_user(user_id, limit)
            return conversations
        except Exception as e:
            logger.error("Error al obtener conversaciones para el usuario %s: %s", user_id, e)
            return []

    def delete_conversation(self, conversation_id):
        """
        Elimina una conversación de la base de datos.

        :param conversation_id: ID de la conversación a eliminar.
        :return: True si la eliminación fue exitosa, False en caso de error.
        """
        try:
            success = self.conversation_repository.delete_conversation(conversation_id)
            if success:
                logger.info("Conversación %s eliminada correctamente.", conversation_id)
            return success
        except Exception as e:
            logger.error("Error al eliminar la conversación %s: %s", conversation_id, e)
            return False
