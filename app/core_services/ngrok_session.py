"""
Path: app/core_services/ngrok_session.py
"""

import subprocess
from app.core_logs.logger_configurator import LoggerConfigurator


class NgrokSession:
    """
    Maneja la creación y finalización de la sesión de ngrok.
    """

    def __init__(self, ngrok_command=None):
        """
        :param ngrok_command: Lista con el comando y argumentos para iniciar ngrok.
        """
        self.logger = LoggerConfigurator().configure()
        if ngrok_command is None:
            ngrok_command = ["ngrok", "http", "5000"]
        self.ngrok_command = ngrok_command
        self.process = None

    def start_session(self):
        """
        Inicia la sesión de ngrok en segundo plano.
        Retorna la instancia del proceso si se inicia correctamente.
        """
        self.logger.info("Iniciando sesión de ngrok con el comando: %s", self.ngrok_command)
        try:
            self.process = subprocess.Popen(
                self.ngrok_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return self.process
        except subprocess.SubprocessError as e:
            self.logger.error("Error al iniciar la sesión de ngrok: %s", e)
            return None

    def terminate_session(self):
        """
        Termina la sesión de ngrok si está activa.
        """
        if self.process:
            self.logger.debug("Terminando la sesión de ngrok...")
            self.process.terminate()
            self.process = None
        else:
            self.logger.debug("No hay sesión activa de ngrok para terminar.")
