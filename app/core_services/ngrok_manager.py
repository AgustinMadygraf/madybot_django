"""
Path: app/core_services/ngrok_manager.py
"""

import subprocess
import time
import requests
from app.core_logs.logger_configurator import LoggerConfigurator


class NgrokManager:
    """
    Clase para iniciar ngrok en segundo plano y obtener la URL pública.
    Si detecta que hay una sesión activa en la cuenta gratuita, la cierra automáticamente.
    """
    def __init__(self,
                 ngrok_command=None,
                 max_retries=10,
                 delay=5,
                 interactive=False):
        """
        Inicializa el administrador de ngrok con la configuración predeterminada.

        :param ngrok_command: Lista con el comando y argumentos para iniciar ngrok.
        :param max_retries: Número máximo de reintentos para obtener la URL.
        :param delay: Segundos de espera entre reintentos.
        :param interactive: Si está en True, usará input() para pausas; si no, se omitirán.
        """
        if ngrok_command is None:
            ngrok_command = ["ngrok", "http", "5000"]
        self.logger = LoggerConfigurator().configure()
        self.ngrok_command = ngrok_command
        self.max_retries = max_retries
        self.delay = delay
        self.interactive = interactive

    def kill_existing_ngrok_sessions(self):
        """
        Mata cualquier sesión activa de ngrok para evitar el error ERR_NGROK_108.
        """
        self.logger.warning("Intentando cerrar sesiones previas de ngrok...")
        try:
            subprocess.run(["ngrok", "kill"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            self.logger.info("Sesiones previas de ngrok finalizadas correctamente.")
        except subprocess.CalledProcessError as e:
            self.logger.error("No se pudo cerrar la sesión de ngrok: %s", e)

    def start_ngrok_and_get_url(self):
        """
        Inicia ngrok y obtiene la URL pública con reintentos.
        Si detecta un error de autenticación, cierra la sesión activa y reintenta.
        """
        self.logger.info("Iniciando ngrok con el comando: %s", self.ngrok_command)

        # Pausa opcional (solo si se requiere entorno interactivo)
        if self.interactive:
            input("0 - Presione una tecla para continuar...")

        # Intentar iniciar ngrok
        process = subprocess.Popen(
            self.ngrok_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Otra pausa opcional
        if self.interactive:
            input("1 - Presione una tecla para continuar...")

        self.logger.info("ngrok iniciado, intentando obtener la URL pública...")

        # Verificamos si ngrok lanzó algún error de autenticación de inmediato
        time.sleep(2)  # Damos tiempo a ngrok para escribir en stderr
        possible_stderr = process.stderr.read(2000)  # Leemos los primeros 2000 caracteres

        if possible_stderr:
            self.logger.error("Salida de error de ngrok (stderr):\n%s", possible_stderr)
            if "ERR_NGROK_108" in possible_stderr or "authentication failed" in possible_stderr:
                self.logger.warning("""
                                    Detectado error de autenticación en ngrok. Cerrando sesiones activas...
                                    """)
                process.terminate()
                self.kill_existing_ngrok_sessions()  # Cerramos sesiones previas

                # Intentamos iniciar ngrok nuevamente
                return self.start_ngrok_and_get_url()

        # Intentamos obtener la URL pública con reintentos
        public_url = None
        for attempt in range(self.max_retries):
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
                self.logger.info("Intento %d: Código de estado %d",
                                 attempt + 1, response.status_code)
                self.logger.debug("Contenido de la respuesta: %s", response.text)

                if response.status_code == 200:
                    tunnels = response.json().get('tunnels', [])
                    for tunnel in tunnels:
                        if tunnel.get('proto') in ['http', 'https']:
                            public_url = tunnel.get('public_url')
                            self.logger.info("URL pública encontrada: %s", public_url)
                            break
                    if public_url:
                        break  # Salimos del bucle si ya la encontramos
                    else:
                        self.logger.error("""
                                          No se encontraron túneles HTTP/HTTPS activos en la respuesta.
                                          """)
                else:
                    self.logger.error("Respuesta inesperada: %s", response.text)
            except requests.exceptions.RequestException as e:
                self.logger.error("Error en el intento %d/%d: %s", attempt + 1, self.max_retries, e)

            time.sleep(self.delay)

        # Finalizamos el proceso de ngrok tras los intentos
        process.terminate()

        if not public_url:
            raise ValueError(f"""
                             No se pudo obtener la URL de ngrok después de {self.max_retries} intentos.
                             """)

        return public_url
