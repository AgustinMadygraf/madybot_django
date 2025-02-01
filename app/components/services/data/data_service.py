"""
Path: app/components/services/data/data_service.py
Servicio para manejar la lógica principal de recepción y procesamiento de datos.
"""

from marshmallow import ValidationError
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.components.services.data.data_validator import DataSchemaValidator
from app.components.services.response.response_generator import ResponseGenerator
from app.components.channels.imessaging_channel import IMessagingChannel
from app.utils.mysql_connector import MySQLConnector
from app.infrastructure.repository import Repository



logger = LoggerConfigurator().configure()

class DataService:
    """
    Servicio que encapsula la lógica de validación y generación de respuesta,
    desacoplándola del framework Flask.
    """

    def __init__(self, validator: DataSchemaValidator,
                 response_generator: ResponseGenerator,
                 channel: IMessagingChannel, db: MySQLConnector, repository: Repository):
        self.validator = validator
        self.response_generator = response_generator
        self.channel = channel
        self.db = db
        self.repository = repository

    def process_incoming_data(self, json_data: dict) -> str:
        """
        Valida los datos entrantes, obtiene el mensaje y decide si la respuesta
        se genera en streaming o de forma normal.
        Retorna el mensaje de respuesta final para ser renderizado.
        """

        # Validar
        logger.info("Validando datos: %s", json_data)
        try:
            valid_data = self.validator.validate(json_data)
        except ValidationError as err:
            logger.warning("Error de validación: %s", err.messages)
            raise

        # Recibir mensaje desde el canal
        processed_data = self.channel.receive_message(valid_data)
        logger.info("Datos procesados desde el canal: %s", processed_data)

        message_text = processed_data.get('message')
        is_stream = processed_data.get('stream', False)

        # Guardar datos del usuario y conversación en la base de datos
        user_data = {
            'id': valid_data.get('user_id'),
            'name': valid_data.get('user_name'),
            'email': valid_data.get('user_email')
        }
        conversation_data = {
            'user_id': valid_data.get('user_id'),
            'message': message_text,
            'response': None  # La respuesta se actualizará después
        }

        self.save_user(user_data)
        conversation_id = self.save_conversation(conversation_data)

        try:
            if is_stream:
                logger.info("Generando respuesta en modo streaming.")
                response = self.response_generator.generate_response_streaming(message_text)
            else:
                logger.info("Generando respuesta en modo normal.")
                response = self.response_generator.generate_response(message_text)

            # Actualizar la respuesta en la base de datos
            self.update_conversation_response(conversation_id, response)
            return response

        except (ValueError, TypeError) as e:
            logger.error("Error procesando la solicitud: %s", e)
            return "Error procesando la solicitud."

    def save_user(self, user_data):
        " Guarda los datos del usuario en la base de datos. "
        query = """
        INSERT INTO users (user_id, user_name, user_email)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE user_name=VALUES(user_name), user_email=VALUES(user_email)
        """
        return self.repository.execute_query(query, (user_data['id'], user_data['name'], user_data['email']))


    def save_conversation(self, conversation_data):
        " Guarda los datos de la conversación en la base de datos. "
        query = "INSERT INTO conversations (user_id, message, response) VALUES (%s, %s, %s)"
        return self.repository.execute_query(query, (conversation_data['user_id'],
                                                     conversation_data['message'], conversation_data['response']))

    def update_conversation_response(self, conversation_id, response):
        " Actualiza la respuesta de la conversación en la base de datos. "
        query = """
        UPDATE conversations
        SET response = %s
        WHERE id = %s
        """
        params = (response, conversation_id)
        self.db.execute_query(query, params)
