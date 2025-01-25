"""
Path: app_flask.py

"""

import sys
import json
from flask import Flask
from flask_cors import CORS
from core.data_controller import data_controller
from core.logs.config_logger import LoggerConfigurator
from core.services.url_service import UrlService

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

# Cargar variables de configuración desde el archivo config.json
try:
    logger.debug("Intentando cargar el archivo config.json")
    with open('config/config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    logger.debug("config.json cargado correctamente")
except FileNotFoundError as e:
    logger.error("Error loading config.json file: %s", e)
    logger.debug("""
                 Asegúrate de que el archivo config.json existe en el directorio config del proyecto
                 """)
    print("Please create a config.json file with the necessary configuration variables.")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Registrar el blueprint del controlador
try:
    app.register_blueprint(data_controller)
    logger.info("Blueprint registrado correctamente.")
except RuntimeError as e:
    logger.error("Error al registrar el blueprint: %s", e)
    sys.exit(1)

# Crear instancia del servicio
url_service = UrlService(config['ENDPOINT_NGROK_PHP'])

if __name__ == '__main__':
    print("Starting Flask server...")
    try:
        url = url_service.get_public_url()
        url_service.save_url(url)
        logger.info("URL enviada correctamente.")
    except (ConnectionError, ValueError) as e:
        logger.error("Error al ejecutar el servicio de URL: %s", e)

    # Finalmente iniciar Flask
    try:
        app.run(debug=config['IS_DEVELOPMENT'], host='0.0.0.0', port=5000)
        logger.info("Servidor configurado para HTTP.")
    except (OSError, RuntimeError) as e:
        logger.error("Error al iniciar el servidor Flask: %s", e)
        sys.exit(1)
