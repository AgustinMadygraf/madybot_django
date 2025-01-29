"""
Path: run_url_remote.py
"""

from app.core_config.flask_config import FlaskConfig
from app.core_logs.logger_configurator import LoggerConfigurator
from app.core_services.url_service import UrlService
from app.core_services.ngrok_manager import NgrokManager

logger = LoggerConfigurator().configure()

def main():
    " Función principal para obtener y guardar la URL de ngrok en un servidor remoto "
    flask_config = FlaskConfig()
    config = flask_config.get_config()
    endpoint_ngrok_php = config['ENDPOINT_NGROK_PHP']

    logger.info("Endpoint NGROK PHP: %s", endpoint_ngrok_php)

    # Crear instancias de servicio y gestor de ngrok
    ngrok_manager = NgrokManager()
    url_service = UrlService(endpoint_ngrok_php)

    logger.info("Iniciando la obtención de la URL de ngrok...")
    public_url = ngrok_manager.start_ngrok_and_get_url()

    logger.info("Guardando la URL pública en el servidor remoto...")
    url_service.save_url(public_url)
    logger.info("URL guardada correctamente: %s", public_url)

if __name__ == "__main__":
    main()
