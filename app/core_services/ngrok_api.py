"""
Path: app/core_services/ngrok_api.py
"""

import requests
from app.core_logs.logger_configurator import LoggerConfigurator


class NgrokAPI:
    """
    Clase para interactuar con la API local de ngrok (generalmente en http://localhost:4040).
    """

    def __init__(self, host="http://localhost:4040", timeout=10):
        self.logger = LoggerConfigurator().configure()
        self.host = host
        self.timeout = timeout

    def get_public_url(self):
        """
        Consulta la API local de ngrok y retorna la primera URL pública disponible
        para protocolos HTTP/HTTPS.
        """
        self.logger.debug("Solicitando lista de túneles a la API de ngrok: %s", self.host)
        try:
            response = requests.get(f"{self.host}/api/tunnels", timeout=self.timeout)
            self.logger.debug("Código de estado: %d", response.status_code)

            if response.status_code == 200:
                tunnels = response.json().get('tunnels', [])
                self.logger.debug("Túneles detectados: %d", len(tunnels))
                for tunnel in tunnels:
                    if tunnel.get('proto') in ['http', 'https']:
                        public_url = tunnel.get('public_url')
                        self.logger.info("URL pública encontrada: %s", public_url)
                        return public_url
                self.logger.error("No se encontraron túneles HTTP/HTTPS activos en la respuesta.")
                return None
            else:
                self.logger.error("Respuesta inesperada de la API: %s", response.text)
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error("Error de conexión con la API de ngrok: %s", e)
            return None
