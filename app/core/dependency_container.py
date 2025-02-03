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

# Importar los nuevos servicios de persistencia
from app.components.services.data.user_persistence_service import UserPersistenceService
from app.components.services.data.conversation_persistence_service import ConversationPersistenceService

class DependencyContainer:
    "Contenedor de dependencias para la inyección de dependencias en la aplicación."
    
    def __init__(self):
        self.web_channel = WebMessagingChannel()
        self.data_validator = DataSchemaValidator()
        self.model_config = ModelConfig()
        self.llm_client = self.model_config.create_llm_client()
        self.response_generator = ResponseGenerator(self.llm_client)

        # Instanciar repositorios
        self.user_repository = UserRepository()
        self.conversation_repository = ConversationRepository()

        # Usar servicios especializados en lugar de PersistenceService
        self.user_persistence_service = UserPersistenceService(self.user_repository)
        self.conversation_persistence_service = ConversationPersistenceService(self.conversation_repository)

        # Pasar los servicios especializados a DataService
        self.data_service = DataService(
            self.data_validator,
            self.response_generator,
            self.web_channel,
            self.user_persistence_service,  # Servicio especializado en usuarios
            self.conversation_persistence_service  # Servicio especializado en conversaciones
        )

container = DependencyContainer()
