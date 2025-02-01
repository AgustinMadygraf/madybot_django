"""
Path: componente_flask/controllers/data_controller.py
Controlador Flask que se encarga de recibir las peticiones HTTP y delegar
la lógica a DataService.
"""

from flask import Blueprint, request, redirect, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from marshmallow import ValidationError
from app.utils.response import render_json_response
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.core.config import FlaskConfig
from app.core.dependency_container import container

data_service = container.data_service

logger = LoggerConfigurator().configure()
load_dotenv()

data_controller = Blueprint('data_controller', __name__)
CORS(data_controller)

flask_config = FlaskConfig()
config = flask_config.get_config()

root_API = config['root_API']
logger.info("Ruta raíz del API: %s", root_API)

@data_controller.route(root_API + '/', methods=['GET'])
@data_controller.route(           '/', methods=['GET'])
def redirect_to_frontend():
    "Redirige al frontend en caso de que se acceda a la raíz del API."
    url_frontend = config['url_frontend']
    return redirect(url_frontend)


@data_controller.route(root_API  +'receive-data'  , methods=['POST', 'HEAD'])
@data_controller.route(root_API  +'receive-data'  , methods=['POST', 'HEAD'])
@data_controller.route('/API/V1/'+'receive-data'  , methods=['POST', 'HEAD'])
@data_controller.route('/API/V1/'+'receive-data/' , methods=['POST', 'HEAD'])
@data_controller.route('/'       + 'receive-data' , methods=['POST', 'HEAD'])
@data_controller.route('/'       + 'receive-data/', methods=['POST', 'HEAD'])
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


@data_controller.route(root_API  + 'health-check' , methods=['GET'])
@data_controller.route(root_API  + 'health-check/', methods=['GET'])
@data_controller.route('/API/V1/'+ 'health-check' , methods=['GET'])
@data_controller.route('/API/V1/'+ 'health-check/', methods=['GET'])
@data_controller.route('/'       + 'health-check' , methods=['GET'])
@data_controller.route('/'       + 'health-check/', methods=['GET'])
def health_check():
    "Verifica que el servidor esté funcionando correctamente."
    logger.info("Health check solicitado. El servidor está funcionando correctamente.")
    return render_json_response(200, "El servidor está operativo.")

@data_controller.route('/save_user', methods=['POST'])
def save_user():
    " Guarda los datos del usuario en la base de datos. "
    user_data = request.json
    user_id = data_service.save_user_data(user_data)
    return jsonify({'user_id': user_id})

@data_controller.route('/save_conversation', methods=['POST'])
def save_conversation():
    " Guarda los datos de la conversación en la base de datos. "
    conversation_data = request.json
    conversation_id = data_service.save_conversation(conversation_data)
    return jsonify({'conversation_id': conversation_id})
