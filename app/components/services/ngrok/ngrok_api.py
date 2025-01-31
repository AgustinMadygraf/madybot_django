"""
Path: app/core_services/ngrok_api.py
"""

import requests
from app.utils.logging.logger_configurator import LoggerConfigurator

class NgrokAPI:
    """Clase para interactuar con la API local de ngrok."""

    def __init__(self):
        self.logger = LoggerConfigurator().configure()
        self.host = "http://localhost:4040"

    def get_public_url(self):
        """Consulta la API local de ngrok y retorna la URL pública."""
        try:
            response = requests.get(f"{self.host}/api/tunnels", timeout=10)
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') in ['http', 'https']:
                    return tunnel.get('public_url')
        except requests.exceptions.RequestException as e:
            self.logger.error("Error al obtener la URL de ngrok: %s", e)
        return None
