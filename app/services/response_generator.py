"""
Path: app/core_services/response_generator.py

"""

from app.utils.logging.logger_configurator import LoggerConfigurator
from app.services.model_config import ModelConfig
from app.services.llm_client import IBaseLLMClient, IStreamingLLMClient
from app.services.business_rules_engine import BusinessRulesEngine

class ResponseGenerator:
    """
    Clase encargada de generar respuestas a partir de un mensaje de entrada.
    Primero consulta las reglas de negocio antes de llamar al LLM.
    """

    def __init__(self, llm_client: IBaseLLMClient = None, custom_logger=None):
        """
        Constructor que admite inyección de dependencia (llm_client).
        Si no se provee, se crea usando ModelConfig (por defecto, Gemini u otro).
        """
        self.logger = custom_logger or LoggerConfigurator().configure()
        self.model_config = ModelConfig(logger=self.logger)
        self.rules_engine = BusinessRulesEngine()  # Capa de reglas de negocio

        # Usa el cliente LLM que se provee, o crea uno por defecto desde ModelConfig
        self.model = llm_client if llm_client else self.model_config.create_llm_client()

        self.logger.info("ResponseGenerator inicializado con un cliente LLM y reglas de negocio.")

    def generate_response(self, message_input: str) -> str:
        """
        Genera una respuesta no-streaming para un mensaje dado.
        Primero revisa las reglas de negocio antes de llamar al LLM.
        """
        self.logger.info(f"Generando respuesta para el mensaje: {message_input}")

        try:
            # Consultar reglas de negocio primero
            rule_response = self.rules_engine.get_response(message_input)
            if rule_response:
                self.logger.info("Respuesta obtenida desde reglas de negocio.")
                return rule_response

            # Si no hay coincidencias en reglas de negocio, llamar al LLM
            return self.model.send_message(message_input)
        except Exception as e:
            self.logger.error("Error al generar respuesta: %s", e)
            raise

    def generate_response_streaming(self, message_input: str, chunk_size: int = 30) -> str:
        """
        Genera una respuesta en modo streaming, si el cliente lo soporta.
        Caso contrario, recurre a la generación no-streaming.
        """
        self.logger.info(f"Generando respuesta en streaming para: {message_input}")

        try:
            if isinstance(self.model, IStreamingLLMClient):
                return self.model.send_message_streaming(message_input, chunk_size)
            return self.generate_response(message_input)
        except Exception as e:
            self.logger.error("Error al generar respuesta en streaming: %s", e)
            raise
