"""
Path: tests/test_data_service.py

"""

from unittest.mock import Mock
from app.components.services.data_service import DataService
from app.components.services.response_generator import ResponseGenerator
from app.components.services.data_validator import DataSchemaValidator
from app.components.channels.imessaging_channel import IMessagingChannel

def test_process_valid_data():
    " Prueba para procesar datos válidos. "
    # Crear mocks
    mock_validator = Mock(spec=DataSchemaValidator)
    mock_response_generator = Mock(spec=ResponseGenerator)
    mock_channel = Mock(spec=IMessagingChannel)

    # Configurar mocks
    mock_validator.validate.return_value = {"message": "Test message"}
    mock_channel.receive_message.return_value = {"message": "Test message", "stream": False}
    mock_response_generator.generate_response.return_value = "Response message"

    # Crear instancia del servicio
    service = DataService(mock_validator, mock_response_generator, mock_channel)

    # Ejecutar prueba
    result = service.process_incoming_data({"message": "Test message"})
    assert result == "Response message"
    mock_validator.validate.assert_called_once()
    mock_channel.receive_message.assert_called_once()
    mock_response_generator.generate_response.assert_called_once()
