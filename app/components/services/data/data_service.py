"""
Path: app/components/services/data/data_service.py
Servicio para manejar la lógica principal de recepción y procesamiento de datos.
"""

from marshmallow import ValidationError
from utils.logging.logger_configurator import LoggerConfigurator
from app.components.services.data.data_validator import DataSchemaValidator
from app.components.services.response.response_generator import ResponseGenerator
from app.components.channels.imessaging_channel import IMessagingChannel
from app.components.services.data.user_persistence_service import UserPersistenceService
from app.components.services.data.conversation_persistence_service import ConversationPersistenceService

logger = LoggerConfigurator().configure()

class DataService:
    "Servicio para manejar la lógica principal de recepción y procesamiento de datos."

    def __init__(self, validator: DataSchemaValidator,
                 response_generator: ResponseGenerator,
                 channel: IMessagingChannel,
                 user_persistence_service: UserPersistenceService,
                 conversation_persistence_service: ConversationPersistenceService):
        self.validator = validator
        self.response_generator = response_generator
        self.channel = channel
        self.user_persistence_service = user_persistence_service
        self.conversation_persistence_service = conversation_persistence_service

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

        # Extraer la información de usuario correctamente desde el campo anidado "user_data"
        user_info = valid_data.get("user_data")
        if not user_info:
            raise KeyError("user_data")

        # Preparar los datos para la conversación
        conversation_data = {
            'user_id': user_info.get("id"),
            'message': message_text,
            'response': None  # La respuesta se actualizará posteriormente
        }

        # Guardar usuario y conversación con los servicios especializados
        self.user_persistence_service.save_user(user_info)
        conversation_id = self.conversation_persistence_service.save_conversation(conversation_data)

        try:
            if is_stream:
                logger.info("Generando respuesta en modo streaming.")
                response = self.response_generator.generate_response_streaming(message_text)
            else:
                logger.info("Generando respuesta en modo normal.")
                response = self.response_generator.generate_response(message_text)

            self.conversation_persistence_service.update_conversation_response(conversation_id, response)
            return response

        except (ValueError, TypeError) as e:
            logger.error("Error procesando la solicitud: %s", e)
            return "Error procesando la solicitud."

    def save_user(self, user_data: dict):
        """
        Método que delega el guardado de usuario a UserPersistenceService.
        """
        logger.info("Datos enviados a user_persistence_service.save_user(): %s", user_data)
        return self.user_persistence_service.save_user(user_data)

    def save_conversation(self, conversation_data: dict):
        """
        Método que delega el guardado de conversación a ConversationPersistenceService.
        """
        return self.conversation_persistence_service.save_conversation(conversation_data)
