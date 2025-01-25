"""
Path: app_flask.py
"""
import sys
from core.config.flask_config import FlaskConfig
from core.data_controller import data_controller
from core.services.url_service import UrlService

# Inicializar la configuración de Flask
flask_config = FlaskConfig()
app = flask_config.create_app()
config = flask_config.get_config()

# Registrar el blueprint del controlador
try:
    app.register_blueprint(data_controller)
    flask_config.logger.info("Blueprint registrado correctamente.")
except RuntimeError as e:
    flask_config.logger.error("Error al registrar el blueprint: %s", e)
    sys.exit(1)

# Crear instancia del servicio
url_service = UrlService(config['ENDPOINT_NGROK_PHP'])

if __name__ == '__main__':
    # print("Starting Flask server...")
    # try:
    #     url = url_service.get_public_url()
    #     url_service.save_url(url)
    #     logger.info("URL enviada correctamente.")
    # except (ConnectionError, ValueError) as e:
    #     logger.error("Error al ejecutar el servicio de URL: %s", e)

    # Finalmente iniciar Flask
    try:
        app.run(debug=config['IS_DEVELOPMENT'], host='0.0.0.0', port=5000)
        flask_config.logger.info("Servidor configurado para HTTP.")
    except (OSError, RuntimeError) as e:
        flask_config.logger.error("Error al iniciar el servidor Flask: %s", e)
        sys.exit(1)
