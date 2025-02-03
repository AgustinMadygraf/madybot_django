"""
Path: app/core/dependency_container.py
Contenedor de dependencias para la inyección de dependencias en la aplicación.
"""

# Importar repositorios especializados en lugar de la clase genérica Repository
from app.repositories.user_repository import UserRepository
from app.repositories.conversation_repository import ConversationRepository
from app.components.services.data.data_service import DataService
from app.components.services.data.data_validator import DataSchemaValidator
from app.components.services.response.response_generator import ResponseGenerator
from app.components.services.llm.model_config import ModelConfig
from app.components.channels.web_messaging_channel import WebMessagingChannel
from app.components.services.data.persistence_service import PersistenceService

class DependencyContainer:
    "Contenedor de dependencias para la inyección de dependencias en la aplicación."
    def __init__(self):
        self.web_channel = WebMessagingChannel()
        self.data_validator = DataSchemaValidator()
        self.model_config = ModelConfig()
        self.llm_client = self.model_config.create_llm_client()
        self.response_generator = ResponseGenerator(self.llm_client)
        # Usar el repositorio especializado para usuarios
        self.user_repository = UserRepository()
        self.conversation_repository = ConversationRepository()
        self.persistence_service = PersistenceService(self.user_repository, self.conversation_repository)
        self.data_service = DataService(
            self.data_validator,
            self.response_generator,
            self.web_channel,
            self.persistence_service
        )

container = DependencyContainer()
