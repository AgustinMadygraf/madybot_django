"""
Path: core/views.py
Este archivo se encarga de manejar las vistas de la aplicación core.
"""

from django.http import JsonResponse
from core.services.data_service import DataService
from core.channels.imessaging_channel import IMessagingChannel

# Inicializa servicios aquí como en Flask
from core.services.data_validator import DataSchemaValidator
from core.services.model_config import ModelConfig
from core.services.response_generator import ResponseGenerator

class WebMessagingChannel(IMessagingChannel):
    # Igual que en Flask
    def send_message(self, msg: str, chat_id: str = None) -> None:
        pass

    def receive_message(self, payload: dict) -> dict:
        return {"message": payload.get('prompt_user'), "stream": payload.get('stream', False)}

# Instancias globales
data_validator = DataSchemaValidator()
model_config = ModelConfig()
llm_client = model_config.create_llm_client()
response_generator = ResponseGenerator(llm_client)
web_channel = WebMessagingChannel()
data_service = DataService(data_validator, response_generator, web_channel)

def receive_data(request):
    if request.method == "HEAD":
        return JsonResponse({}, status=200)

    if request.method == "POST":
        try:
            json_data = request.body.decode('utf-8')  # Lee el cuerpo como JSON
            response_message = data_service.process_incoming_data(json_data)
            return JsonResponse({"response_MadyBot": response_message}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def health_check(request):
    return JsonResponse({"status": "El servidor está operativo"}, status=200)

def home(request):
    return JsonResponse({"message": "Bienvenido a MadyBot"}, status=200)
