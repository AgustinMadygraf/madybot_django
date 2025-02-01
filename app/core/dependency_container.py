"""
Path: app/core/dependency_container.py
Contenedor de dependencias para la inyección de dependencias en la aplicación.
"""

from app.utils.mysql_connector import MySQLConnector
from app.components.services.data.data_service import DataService
from app.components.services.data.data_validator import DataSchemaValidator
from app.components.services.response.response_generator import ResponseGenerator
from app.components.services.llm.model_config import ModelConfig
from app.components.channels.web_messaging_channel import WebMessagingChannel
from app.infrastructure.repository import Repository

class DependencyContainer:
    " Contenedor de dependencias para la inyección de dependencias en la aplicación. "
    def __init__(self):
        self.db = MySQLConnector()
        self.web_channel = WebMessagingChannel()
        self.data_validator = DataSchemaValidator()
        self.model_config = ModelConfig()
        self.llm_client = self.model_config.create_llm_client()
        self.response_generator = ResponseGenerator(self.llm_client)
        self.repository = Repository()
        self.data_service = DataService(self.data_validator, self.response_generator, self.web_channel, self.db, self.repository)

container = DependencyContainer()
