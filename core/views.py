"""
Path: core/views.py
Vista principal de la app Django que ahora usa la configuración centralizada
'ModelConfig' desde 'componente_flask/services/model_config.py'.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Servicios y lógica adicional
from core.channels.imessaging_channel import IMessagingChannel
from core.logs.dependency_injection import app_logger
from core.services.data_validator import DataSchemaValidator
from core.services.data_service import DataService
from core.services.response_generator import ResponseGenerator

# IMPORTACIÓN NUEVA: usar el model_config "unificado" de componente_flask
from componente_flask.services.model_config import ModelConfig


class WebMessagingChannel(IMessagingChannel):
    """
    Canal de mensajería que cumple con la interfaz IMessagingChannel.
    Se limita a simular el envío/recepción de mensajes en un contexto web.
    """
    def send_message(self, msg: str, chat_id: str = None) -> None:
        app_logger.debug(f"Enviando mensaje: {msg} al chat ID: {chat_id}")
        # Aquí podrías implementar la lógica de envío real (websockets, etc.)
        pass

    def receive_message(self, payload: dict) -> dict:
        app_logger.debug(f"Recibiendo payload: {payload}")
        return {"message": payload.get("prompt_user"), "stream": payload.get("stream", False)}


# =====================
#  Instancias globales
# =====================

data_validator = DataSchemaValidator()

# Configuración del modelo unificada
model_config = ModelConfig(logger=app_logger)
llm_client = model_config.create_llm_client()

# Se asume que ResponseGenerator ya puede trabajar directamente con un llm_client + logger
response_generator = ResponseGenerator(llm_client, app_logger)

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
