"""
Path: app/services/llm_impl/DeepSeek_llm.py

Implementación de IBaseLLMClient utilizando la API de DeepSeek.
No se maneja streaming, por lo que solo implementa envío de mensaje.
"""

import os
from openai import OpenAI, AuthenticationError, OpenAIError
from dotenv import load_dotenv
from app.services.llm_client import IBaseLLMClient
from app.utils.logging.logger_configurator import LoggerConfigurator

# Cargar API key desde variables de entorno
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

class DeepSeekLLMClient(IBaseLLMClient):
    """
    Cliente para la API de DeepSeek, implementando únicamente envío de mensajes.
    """
    def __init__(self, logger=None):
        self.logger = logger if logger else LoggerConfigurator().configure()

        if not api_key:
            raise ValueError("API key not found. Please set DEEPSEEK_API_KEY environment variable.")

        self.logger.info("Usando API Key para DeepSeek: %s", api_key)

        # Inicializar el cliente de OpenAI con base_url de DeepSeek
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def send_message(self, message: str) -> str:
        """
        Envía un mensaje (sin streaming) y devuelve el texto de la respuesta.
        """
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": message},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except AuthenticationError as e:
            err_msg = f"AuthenticationError en DeepSeek: {e}"
            self.logger.error(err_msg)
            raise
        except OpenAIError as e:
            # Manejar caso de saldo insuficiente u otros errores
            if "Insufficient Balance" in str(e):
                err_msg = "OpenAIError: Insufficient Balance en DeepSeek."
            else:
                err_msg = f"OpenAIError en DeepSeek: {e}"
            self.logger.error(err_msg)
            raise
