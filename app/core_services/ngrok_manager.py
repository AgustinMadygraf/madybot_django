"""
Path: app/core_services/ngrok_manager.py
"""

import time
from app.core_logs.logger_configurator import LoggerConfigurator
from app.core_services.ngrok_session import NgrokSession
from app.core_services.ngrok_error_handler import NgrokErrorHandler
from app.core_services.ngrok_api import NgrokAPI


class NgrokManager:
    """
    Clase que coordina el inicio de ngrok, la detección de errores y
    la obtención de la URL pública.
    """

    def __init__(self, ngrok_command=None, max_retries=10, delay=5, restart_delay=5):
        """
        :param ngrok_command: Lista con el comando y argumentos para iniciar ngrok.
        :param max_retries: Número máximo de reintentos para obtener la URL.
        :param delay: Segundos de espera entre intentos de obtención de la URL.
        :param restart_delay: Segundos de espera después de reiniciar ngrok antes de intentar obtener la URL.
        """
        self.logger = LoggerConfigurator().configure()
        self.ngrok_session = NgrokSession(ngrok_command)
        self.ngrok_error_handler = NgrokErrorHandler()
        self.ngrok_api = NgrokAPI()
        self.max_retries = max_retries
        self.delay = delay
        self.restart_delay = restart_delay  # Nueva espera después de reiniciar ngrok

    def start_ngrok_and_get_url(self):
        """
        Inicia ngrok y obtiene la URL pública con reintentos.
        Si detecta un error de autenticación, cierra la sesión activa y reintenta.
        """
        process = self.ngrok_session.start_session()
        if not process:
            self.logger.error("No se pudo iniciar la sesión de ngrok. Abortando.")
            return None

        # Esperar un poco para ver si ngrok arroja errores en stderr
        time.sleep(2)
        self.logger.debug("Revisando posibles errores iniciales en ngrok...")

        # Lectura no bloqueante de stderr
        possible_stderr = process.stderr.read()
        self.logger.debug("Salida de error capturada:\n%s", possible_stderr)

        # Detectar si hay error de autenticación
        if self.ngrok_error_handler.detect_auth_error(possible_stderr):
            self.logger.warning("Cerrando proceso actual e intentando reiniciar ngrok...")
            self.ngrok_session.terminate_session()
            self.ngrok_error_handler.kill_existing_sessions()

            # Nueva espera para asegurar que ngrok se cerró correctamente
            self.logger.info("Esperando %d segundos antes de reiniciar ngrok...", self.restart_delay)
            time.sleep(self.restart_delay)

            return self.start_ngrok_and_get_url()

        # Nueva espera para asegurarse de que la API de ngrok esté disponible antes de obtener la URL
        self.logger.info("Esperando %d segundos antes de consultar la API de ngrok...", self.restart_delay)
        time.sleep(self.restart_delay)

        # Intentar obtener la URL pública con reintentos
        public_url = None
        for attempt in range(self.max_retries):
            self.logger.debug("Intento %d/%d para obtener la URL pública...", attempt + 1, self.max_retries)
            url = self.ngrok_api.get_public_url()
            if url:
                public_url = url
                break
            time.sleep(self.delay)

        if not public_url:
            self.logger.error("No se pudo obtener la URL de ngrok tras %d intentos", self.max_retries)
            return None

        return public_url
