"""
Path: app/components/services/ngrok/ngrok_coordinator.py

"""

import time
import subprocess
from app.config import FlaskConfig
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.components.services.ngrok.ngrok_manager import NgrokManager
from app.components.url.url_service import UrlService

logger = LoggerConfigurator().configure()

class NgrokCoordinator:
    """
    Clase que orquesta la ejecución de ngrok y la gestión de su URL pública.
    """

    def __init__(self):
        self.flask_config = FlaskConfig()
        self.config = self.flask_config.get_config()
        self.endpoint_ngrok_php = self.config['ENDPOINT_NGROK_PHP']
        self.logger = LoggerConfigurator().configure()
        self.ngrok_manager = NgrokManager()
        self.url_service = UrlService(self.endpoint_ngrok_php)

    def execute(self):
        """Inicia ngrok, obtiene la URL y la guarda en el servidor remoto."""
        print("\033[H\033[J")  # Limpiar pantalla en terminal

        self.logger.info("Iniciando ngrok en segundo plano...")

        try:
            subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(3)
        except subprocess.SubprocessError as e:
            self.logger.error("Error al iniciar ngrok: %s", e)
            return

        self.logger.info("Obteniendo la URL de ngrok...")
        public_url = self.ngrok_manager.start_ngrok_and_get_url()

        if public_url:
            self.logger.info("Guardando la URL pública en el servidor remoto...")
            self.logger.info("URL: %s", public_url)
            self.url_service.save_url(public_url)
            self.logger.info("URL guardada correctamente: %s", public_url)
        else:
            self.logger.error("No se pudo obtener la URL de ngrok.")

        self.logger.info("Túnel de ngrok activo. Para detenerlo, usa 'ngrok kill'.")
        while True:
            time.sleep(1)
            #actualizar los valores de localhost:4040

