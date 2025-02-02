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
        Se espera que user_data tenga la siguiente estructura:
        {
          "id": "<UUID>",
          "browserData": {
              "userAgent": "...",
              "screenResolution": "...",
              "language": "...",
              "platform": "..."
          }
        }
        """
        query = """
        INSERT INTO usuarios (id, userAgent, screenResolution, language, platform)
        VALUES (:id, :userAgent, :screenResolution, :language, :platform)
        ON DUPLICATE KEY UPDATE
          userAgent = VALUES(userAgent),
          screenResolution = VALUES(screenResolution),
          language = VALUES(language),
          platform = VALUES(platform)
        """
        params = {
            'id': user_data['id'],
            'userAgent': user_data['browserData']['userAgent'],
            'screenResolution': user_data['browserData']['screenResolution'],
            'language': user_data['browserData']['language'],
            'platform': user_data['browserData']['platform']
        }
        result = self.repository.execute_query(query, params)
        logger.info("Usuario guardado/actualizado: %s", user_data['id'])
        return result

    def save_conversation(self, conversation_data: dict):
        """
        Guarda los datos de la conversación en la base de datos.
        """
        query = "INSERT INTO conversations (user_id, message, response) VALUES (:user_id, :message, :response)"
        params = {
            'user_id': conversation_data['user_id'],
            'message': conversation_data['message'],
            'response': conversation_data['response']
        }
        result = self.repository.execute_query(query, params)
        logger.info("Conversación guardada para el usuario: %s", conversation_data['user_id'])
        return result

    def update_conversation_response(self, conversation_id, response):
        """
        Actualiza la respuesta de una conversación en la base de datos.
        """
        query = """
        UPDATE conversations
        SET response = :response
        WHERE id = :id
        """
        params = {'response': response, 'id': conversation_id}
        self.repository.execute_query(query, params)
        logger.info("Respuesta actualizada para conversación ID: %s", conversation_id)
