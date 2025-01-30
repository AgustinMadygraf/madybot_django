"""
Path: app/core_services/ngrok_session.py
"""

import subprocess
from app.utils.logging.logger_configurator import LoggerConfigurator

class NgrokSession:
    """Maneja la creación y finalización de la sesión de ngrok."""

    def __init__(self):
        self.logger = LoggerConfigurator().configure()
        self.ngrok_command = ["ngrok", "http", "5000"]
        self.process = None

    def start_session(self):
        """Inicia la sesión de ngrok en segundo plano."""
        try:
            self.logger.info("Iniciando ngrok...")
            self.process = subprocess.Popen(self.ngrok_command,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return self.process
        except subprocess.SubprocessError as e:
            self.logger.error("Error al iniciar ngrok: %s", e)
            return None
