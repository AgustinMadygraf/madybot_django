"""
Path: app/components/services/data/data_service.py
Servicio para manejar la lógica principal de recepción y procesamiento de datos.
"""

from marshmallow import ValidationError
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.components.services.data.data_validator import DataSchemaValidator
from app.components.services.response.response_generator import ResponseGenerator
from app.components.channels.imessaging_channel import IMessagingChannel
from app.infrastructure.database_connection import DatabaseConnection

logger = LoggerConfigurator().configure()

class DataService:
    def __init__(self, validator: DataSchemaValidator,
                 response_generator: ResponseGenerator,
                 channel: IMessagingChannel,
                 persistence_service):  # ✅ No incluir `db`
        self.validator = validator
        self.response_generator = response_generator
        self.channel = channel
        self.persistence_service = persistence_service


    def process_incoming_data(self, json_data: dict) -> str:
        """
        Valida los datos entrantes, obtiene el mensaje y decide si la respuesta
        se genera en streaming o de forma normal.
        Retorna el mensaje de respuesta final para ser renderizado.
        """
        logger.info("Validando datos: %s", json_data)
        try:
            valid_data = self.validator.validate(json_data)
        except ValidationError as err:
            logger.warning("Error de validación: %s", err.messages)
            raise

        processed_data = self.channel.receive_message(valid_data)
        logger.info("Datos procesados desde el canal: %s", processed_data)

        message_text = processed_data.get('message')
        is_stream = processed_data.get('stream', False)

        # Preparar datos para persistencia
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

        self.persistence_service.save_user(user_data)
        conversation_id = self.persistence_service.save_conversation(conversation_data)

        try:
            if is_stream:
                logger.info("Generando respuesta en modo streaming.")
                response = self.response_generator.generate_response_streaming(message_text)
            else:
                logger.info("Generando respuesta en modo normal.")
                response = self.response_generator.generate_response(message_text)

            self.persistence_service.update_conversation_response(conversation_id, response)
            return response

        except (ValueError, TypeError) as e:
            logger.error("Error procesando la solicitud: %s", e)
            return "Error procesando la solicitud."
