"""
Path: services/url_service.py

"""

import subprocess
import time
import requests
from core.logs.logger_configurator import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

class UrlService:
    " Servicio para obtener y guardar la URL pública de ngrok "
    def __init__(self, endpoint_ngrok_php):
        self.endpoint_ngrok_php = endpoint_ngrok_php

    def get_public_url(self):
        """
        Obtiene la URL pública de ngrok.
        """
        url = get_url_ngrok()
        if not url:
            raise ValueError("No se pudo obtener la URL de ngrok")
        return url

    def save_url(self, url):
        """
        Guarda la URL pública en un servidor remoto.
        """
        if not url:
            raise ValueError("La URL proporcionada está vacía")
        save_url(url, self.endpoint_ngrok_php)

def save_url(url_to_save, endpoint):
    "Envía una URL a un servidor remoto"
    # Datos a enviar
    data = {
        'url': url_to_save
    }
    try:
        # Realizar la petición POST
        response = requests.post(endpoint, data=data, timeout=10)
        # Verificar si la petición fue exitosa
        if response.status_code == 200:
            print("URL enviada exitosamente")
        else:
            print(f"Error: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición: {e}")

def get_url_ngrok():
    """
    Obtiene la URL pública de ngrok con un bucle de reintentos.
    Incluye soporte para túneles HTTPS y manejo de errores adicionales.
    """
    try:
        # Iniciar ngrok en segundo plano
        subprocess.Popen(["ngrok", "http", "5000"])
        logger.debug("ngrok iniciado, intentando obtener la URL pública...")

        # Intentar obtener la URL pública con reintentos
        max_retries = 10  # Número máximo de intentos
        delay = 5  # Tiempo en segundos entre intentos
        for attempt in range(max_retries):
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
                logger.debug("Intento %d: Código de estado %d", attempt + 1, response.status_code)
                logger.debug("Contenido completo de la respuesta: %s", response.json())

                if response.status_code == 200:
                    tunnels = response.json().get('tunnels', [])
                    for tunnel in tunnels:
                        # Aceptar tanto túneles HTTP como HTTPS
                        if tunnel.get('proto') in ['http', 'https']:
                            logger.info("URL pública encontrada: %s", tunnel.get('public_url'))
                            return tunnel.get('public_url')
                    logger.error("No se encontraron túneles HTTP/HTTPS activos en la respuesta.")
                else:
                    logger.error("Respuesta inesperada: %s", response.text)
            except requests.exceptions.RequestException as e:
                logger.error("Intento %d/%d fallido: %s", attempt + 1, max_retries, e)

            time.sleep(delay)

        # Si no se pudo obtener la URL después de los intentos
        raise ValueError(f"No se pudo obtener la URL de ngrok después de {max_retries} intentos.")
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Error al iniciar ngrok: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error inesperado al obtener la URL de ngrok: {e}") from e
