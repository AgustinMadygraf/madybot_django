"""
Path: run_url_remote.py
"""

import time
import subprocess
from app.core_config.flask_config import FlaskConfig
from app.core_logs.logger_configurator import LoggerConfigurator
from app.core_services.url_service import UrlService
from app.core_services.ngrok_manager import NgrokManager

logger = LoggerConfigurator().configure()

def main():
    " Función principal para obtener y guardar la URL de ngrok en un servidor remoto "
    print("\033[H\033[J")  # Limpiar pantalla en terminal

    flask_config = FlaskConfig()
    config = flask_config.get_config()
    endpoint_ngrok_php = config['ENDPOINT_NGROK_PHP']

    logger.info("Endpoint NGROK PHP: %s", endpoint_ngrok_php)

    # Crear instancias de servicio y gestor de ngrok
    ngrok_manager = NgrokManager()
    url_service = UrlService(endpoint_ngrok_php)

    logger.info("Iniciando ngrok en segundo plano...")

    # Ejecutar ngrok sin bloquear el script
    try:
        subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)  # Esperar unos segundos para que el túnel se establezca
    except subprocess.SubprocessError as e:
        logger.error("Error al iniciar ngrok en segundo plano: %s", e)
        return

    logger.info("Obteniendo la URL de ngrok...")
    public_url = ngrok_manager.start_ngrok_and_get_url()

    if public_url:
        logger.info("Guardando la URL pública en el servidor remoto...")
        url_service.save_url(public_url)
        logger.info("URL guardada correctamente: %s", public_url)
    else:
        logger.error("No se pudo obtener la URL de ngrok.")

    logger.info("El túnel de ngrok está activo. Para detenerlo, usa 'ngrok kill' en la terminal.")

if __name__ == "__main__":
    main()
