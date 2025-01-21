"""
Path: core/dependency_injection.py
Contenedor de dependencias para inyección de dependencias.
"""

from core.logs.logging_setup import app_logger
from core.services.llm_impl.gemini_llm import GeminiLLMClient
from core.services.response_generator import ResponseGenerator
from core.services.data_service import DataService


def get_logger():
    "Esta función es un ejemplo de cómo se puede inyectar una dependencia."
    return app_logger


def get_gemini_client(api_key, system_instruction):
    "Esta función es un ejemplo de cómo se puede inyectar una dependencia."
    logger = get_logger()
    return GeminiLLMClient(api_key, system_instruction, logger)


def get_response_generator(model_config):
    "Esta función es un ejemplo de cómo se puede inyectar una dependencia."
    logger = get_logger()
    return ResponseGenerator(model_config, logger)


def get_data_service(validator, response_generator, channel):
    "Esta función es un ejemplo de cómo se puede inyectar una dependencia."
    logger = get_logger()
    return DataService(validator, response_generator, channel, logger)
