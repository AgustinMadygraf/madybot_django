"""
Path: core/views.py
Este archivo se encarga de manejar las vistas de la aplicación core.
"""

from django.http import JsonResponse
from core.services.data_service import DataService
from core.channels.imessaging_channel import IMessagingChannel
from django.views.decorators.csrf import csrf_exempt
from core.services.data_validator import DataSchemaValidator
from core.services.model_config import ModelConfig
from core.services.response_generator import ResponseGenerator
from core.logs.dependency_injection import app_logger


class WebMessagingChannel(IMessagingChannel):
    """Implementación del canal de mensajería basado en IMessagingChannel."""

    def send_message(self, msg: str, chat_id: str = None) -> None:
        app_logger.debug(f"Enviando mensaje: {msg} al chat ID: {chat_id}")
        pass

    def receive_message(self, payload: dict) -> dict:
        app_logger.debug(f"Recibiendo payload: {payload}")
        return {"message": payload.get('prompt_user'), "stream": payload.get('stream', False)}


# Instancias globales
data_validator = DataSchemaValidator()
model_config = ModelConfig()
llm_client = model_config.create_llm_client()
response_generator = ResponseGenerator(llm_client, app_logger)  # Usar el logger importado
web_channel = WebMessagingChannel()
data_service = DataService(data_validator, response_generator, web_channel, app_logger)  # Usar el logger


@csrf_exempt
def receive_data(request):
    """Esta vista recibe los datos del cliente y envía una respuesta."""
    app_logger.debug(f"Recibiendo solicitud: {request.method}")
    
    if request.method == "POST":
        app_logger.info("Solicitud POST recibida correctamente.")
        return JsonResponse({"message": "Solicitud recibida con éxito"}, status=200)

    app_logger.warning("Método no permitido.")
    return JsonResponse({"error": "Método no permitido"}, status=405)


def health_check(request):
    app_logger.debug("Verificando el estado del servidor.")
    app_logger.info("El servidor está operativo.")
    return JsonResponse({"status": "El servidor está operativo"}, status=200)


def home(request):
    app_logger.debug("Acceso a la vista 'home'")
    return JsonResponse({"message": "Bienvenido a MadyBot"}, status=200)
