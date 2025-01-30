"""
Path: app/core_services/ngrok_manager.py
"""

import time
from app.core_logs.logger_configurator import LoggerConfigurator
from app.core_services.ngrok_session import NgrokSession
from app.core_services.ngrok_api import NgrokAPI

class NgrokManager:
    """Clase que coordina el inicio de ngrok y la obtención de la URL pública."""

    def __init__(self, max_retries=10, delay=5):
        self.logger = LoggerConfigurator().configure()
        self.ngrok_session = NgrokSession()
        self.ngrok_api = NgrokAPI()
        self.max_retries = max_retries
        self.delay = delay

    def start_ngrok_and_get_url(self):
        """Inicia ngrok y obtiene la URL pública con reintentos."""
        process = self.ngrok_session.start_session()
        if not process:
            self.logger.error("No se pudo iniciar la sesión de ngrok. Abortando.")
            return None

        self.logger.info("Esperando para obtener la URL pública...")
        self.logger.info("http://localhost:4040 para ver el dashboard de ngrok.")
        time.sleep(2)

        for attempt in range(self.max_retries):
            self.logger.debug("Intento %d/%d para obtener la URL pública...", attempt+1, self.max_retries)
            url = self.ngrok_api.get_public_url()
            if url:
                return url
            time.sleep(self.delay)

        self.logger.error("No se pudo obtener la URL de ngrok tras múltiples intentos.")
        return None
