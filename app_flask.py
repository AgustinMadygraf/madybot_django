"""
Path: app_flask.py
"""

import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from core.data_controller import data_controller
from core.logs.config_logger import LoggerConfigurator
from core.services.url_service import UrlService

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

# Cargar variables de entorno desde el archivo .env
try:
    logger.debug("Intentando cargar el archivo .env")
    if not load_dotenv():
        raise FileNotFoundError(".env file not found")
    logger.debug(".env file cargado correctamente")
except FileNotFoundError as e:
    logger.error("Error loading .env file: %s", e)
    logger.debug("Asegúrate de que el archivo .env existe en el directorio raíz del proyecto")
    print("Please create a .env file with the necessary environment variables.")
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
url_service = UrlService()

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
        app.run(debug=False, host='0.0.0.0', port=5000)
        logger.info("Servidor configurado para HTTP.")
    except (OSError, RuntimeError) as e:
        logger.error("Error al iniciar el servidor Flask: %s", e)
        sys.exit(1)
