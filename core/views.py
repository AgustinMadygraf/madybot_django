from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.channels.imessaging_channel import IMessagingChannel
from core.logs.dependency_injection import app_logger
from core.services.data_validator import DataSchemaValidator
from core.services.data_service import DataService
from core.services.model_config import ModelConfig

# Use the new unified response generator
from core.services.response_generator import ResponseGenerator

class WebMessagingChannel(IMessagingChannel):
    def send_message(self, msg: str, chat_id: str = None) -> None:
        app_logger.debug(f"Sending message: {msg} to chat ID: {chat_id}")
        pass

    def receive_message(self, payload: dict) -> dict:
        app_logger.debug(f"Receiving payload: {payload}")
        return {"message": payload.get("prompt_user"), "stream": payload.get("stream", False)}

# Global instances
data_validator = DataSchemaValidator()
model_config = ModelConfig(logger=app_logger)
response_generator = ResponseGenerator(logger=app_logger)
web_channel = WebMessagingChannel()
data_service = DataService(
    validator=data_validator,
    response_generator=response_generator,
    channel=web_channel,
    logger=app_logger
)


@csrf_exempt
def receive_data(request):
    """
    Esta vista recibe los datos del cliente (POST) y envía una respuesta
    (por ahora sencilla, meramente de ejemplo).
    """
    app_logger.debug(f"Recibiendo solicitud: {request.method}")

    if request.method == "POST":
        app_logger.info("Solicitud POST recibida correctamente.")
        # Aquí se podría llamar a data_service.process_incoming_data(request.json) si fuera necesario.
        return JsonResponse({"message": "Solicitud recibida con éxito"}, status=200)

    app_logger.warning("Método no permitido.")
    return JsonResponse({"error": "Método no permitido"}, status=405)


def health_check(request):
    """
    Verifica el estado del servidor.
    """
    app_logger.debug("Verificando el estado del servidor.")
    app_logger.info("El servidor está operativo.")
    return JsonResponse({"status": "El servidor está operativo"}, status=200)


def home(request):
    """
    Vista de bienvenida simple.
    """
    app_logger.debug("Acceso a la vista 'home'")
    return JsonResponse({"message": "Bienvenido a MadyBot"}, status=200)
