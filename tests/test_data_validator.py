"""
Path: tests/test_data_validator.py

"""

import pytest
from marshmallow.exceptions import ValidationError
from core.services.data_validator import DataSchemaValidator

@pytest.fixture
def valid_data():
    " Fixture para datos válidos. "
    return {
        "prompt_user": "¿Cuál es el stock actual?",
        "stream": False,
        "user_data": {
            "id": "user123",
            "browserData": {
                "userAgent": "Mozilla/5.0",
                "screenResolution": "1920x1080",
                "language": "es",
                "platform": "Windows"
            }
        },
        "datetime": 1672444800
    }

@pytest.fixture
def invalid_data():
    " Fixture para datos inválidos. "
    return {
        "prompt_user": "Un mensaje muy largo" * 100,  # Excede los 255 caracteres
        "stream": "not_boolean",  # Valor no válido
        "user_data": {}
    }

def test_valid_data(valid_data):
    " Prueba para datos válidos. "
    validator = DataSchemaValidator()
    result = validator.validate(valid_data)
    assert result["prompt_user"] == "¿Cuál es el stock actual?"

def test_invalid_data(invalid_data):
    " Prueba para datos inválidos. "
    validator = DataSchemaValidator()
    with pytest.raises(ValidationError):
        validator.validate(invalid_data)
