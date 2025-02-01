"""
Path: app/components/services/data/persistence_service.py
Servicio encargado de las operaciones de persistencia en la base de datos para usuarios y conversaciones.
"""

from app.infrastructure.repository import Repository
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class PersistenceService:
    """
    Servicio para gestionar la persistencia de datos en la base de datos.
    Se encarga de operaciones de inserción y actualización para usuarios y conversaciones.
    """
    def __init__(self, repository: Repository):
        self.repository = repository

    def save_user(self, user_data: dict):
        """
        Guarda o actualiza los datos del usuario en la base de datos.
        """
        query = """
        INSERT INTO users (user_id, user_name, user_email)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE user_name=VALUES(user_name), user_email=VALUES(user_email)
        """
        result = self.repository.execute_query(query, (user_data['id'], user_data['name'], user_data['email']))
        logger.info("Usuario guardado/actualizado: %s", user_data['id'])
        return result

    def save_conversation(self, conversation_data: dict):
        """
        Guarda los datos de la conversación en la base de datos.
        """
        query = "INSERT INTO conversations (user_id, message, response) VALUES (%s, %s, %s)"
        result = self.repository.execute_query(query, (conversation_data['user_id'],
                                                       conversation_data['message'],
                                                       conversation_data['response']))
        logger.info("Conversación guardada para el usuario: %s", conversation_data['user_id'])
        return result

    def update_conversation_response(self, conversation_id, response):
        """
        Actualiza la respuesta de una conversación en la base de datos.
        """
        query = """
        UPDATE conversations
        SET response = %s
        WHERE id = %s
        """
        params = (response, conversation_id)
        self.repository.execute_query(query, params)
        logger.info("Respuesta actualizada para conversación ID: %s", conversation_id)
