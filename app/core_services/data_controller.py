"""
Path: componente_flask/controllers/data_controller.py
Controlador Flask que se encarga de recibir las peticiones HTTP y delegar
la lógica a DataService.
"""

import os
from flask import Blueprint, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from marshmallow import ValidationError
from app.core_utils.response import render_json_response
from app.core_logs.logger_configurator import LoggerConfigurator

# Services y canales
from app.core_services.data_service import DataService
from app.core_services.data_validator import DataSchemaValidator
from app.core_services.model_config import ModelConfig
from app.core_services.response_generator import ResponseGenerator
from app.core_channels.web_messaging_channel import WebMessagingChannel

logger = LoggerConfigurator().configure()
load_dotenv()

data_controller = Blueprint('data_controller', __name__)
CORS(data_controller)


# Instanciar servicios y canal
web_channel = WebMessagingChannel()
data_validator = DataSchemaValidator()

# Crear cliente LLM y ResponseGenerator
model_config = ModelConfig()
llm_client = model_config.create_llm_client()
response_generator = ResponseGenerator(llm_client)

# Crear DataService que unifica validación y respuesta
data_service = DataService(
    validator=data_validator,
    response_generator=response_generator,
    channel=web_channel
)

root_API = os.getenv('ROOT_API', '/')

@data_controller.route(root_API, methods=['GET'])
def redirect_to_frontend():
    "Redirige al frontend en caso de que se acceda a la raíz del API."
    url_frontend = os.getenv('URL_FRONTEND')
    return redirect(url_frontend)

@data_controller.route(root_API + 'receive-data', methods=['POST', 'HEAD'])
def receive_data():
    "Recibe los datos de la solicitud y los procesa con el DataService."
    if request.method == 'HEAD':
        return '', 200

    try:
        logger.info("Request JSON: \n| %s \n", request.json)
        # Procesar la data con nuestro DataService
        response_message = data_service.process_incoming_data(request.json)
        logger.info("Respuesta generada: %s", response_message)
        return render_json_response(200, response_message, stream=False)

    except ValidationError as ve:
        logger.error("Error de validación: %s", ve)
        return render_json_response(400, "Datos inválidos en la solicitud.", stream=False)
    except KeyError as ke:
        logger.error("Error de clave: %s", ke)
        return render_json_response(400, "Clave faltante en la solicitud.", stream=False)
    except TypeError as te:
        logger.error("Error de tipo: %s", te)
        return render_json_response(400, "Tipo de dato incorrecto en la solicitud.", stream=False)
    
@data_controller.route(root_API + 'receive-data/', methods=['POST', 'HEAD'])
def receive_data2():
    "Recibe los datos de la solicitud y los procesa con el DataService."
    if request.method == 'HEAD':
        return '', 200

    try:
        logger.info("Request JSON: \n| %s \n", request.json)
        # Procesar la data con nuestro DataService
        response_message = data_service.process_incoming_data(request.json)
        logger.info("Respuesta generada: %s", response_message)
        return render_json_response(200, response_message, stream=False)

    except ValidationError as ve:
        logger.error("Error de validación: %s", ve)
        return render_json_response(400, "Datos inválidos en la solicitud.", stream=False)
    except KeyError as ke:
        logger.error("Error de clave: %s", ke)
        return render_json_response(400, "Clave faltante en la solicitud.", stream=False)
    except TypeError as te:
        logger.error("Error de tipo: %s", te)
        return render_json_response(400, "Tipo de dato incorrecto en la solicitud.", stream=False)


@data_controller.route(root_API + 'health-check', methods=['GET'])
def health_check():
    "Verifica que el servidor esté funcionando correctamente."
    logger.info("Health check solicitado. El servidor está funcionando correctamente.")
    return render_json_response(200, "El servidor está operativo.")

@data_controller.route(root_API + 'health-check/', methods=['GET'])
def health_check2():
    "Verifica que el servidor esté funcionando correctamente."
    logger.info("Health check solicitado. El servidor está funcionando correctamente.")
    return render_json_response(200, "El servidor está operativo.")
