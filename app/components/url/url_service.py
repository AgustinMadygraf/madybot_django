"""
Path: app/core_services/url_service.py

"""

import requests
from utils.logging.logger_configurator import LoggerConfigurator

class UrlService:
    """Servicio para obtener y guardar la URL pública de ngrok en un servidor remoto."""

    def __init__(self, endpoint_ngrok_php):
        self.endpoint_ngrok_php = endpoint_ngrok_php
        self.logger = LoggerConfigurator().configure()

    def save_url(self, public_url):
        """Guarda la URL pública en un servidor remoto."""
        if not public_url:
            raise ValueError("La URL proporcionada está vacía")

        self.logger.info("Enviando URL al servidor remoto...")
        self.logger.info("URL: %s", public_url)
        self.logger.info("Endpoint: %s", self.endpoint_ngrok_php)
        self.logger.info("Enviando petición...")
        try:
            response = requests.get(self.endpoint_ngrok_php, params={'url': public_url}, timeout=10)
            self.logger.info("Petición realizada a: %s con URL = %s", self.endpoint_ngrok_php, public_url)
            self.logger.info("Respuesta: %s", response.text)
            if response.status_code == 200:
                self.logger.info("URL enviada exitosamente.")
            else:
                self.logger.error("Error en la petición: %s", response.status_code)
        except requests.exceptions.RequestException as e:
            self.logger.error("Error al realizar la petición: %s", e)
