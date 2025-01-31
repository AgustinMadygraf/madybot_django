"""
Path: app/core_services/ngrok_error_handler.py
"""

import subprocess
import time
import platform
from app.utils.logging.logger_configurator import LoggerConfigurator


class NgrokErrorHandler:
    """
    Maneja errores comunes de ngrok, como ERR_NGROK_108 (autenticación fallida o sesión simultánea).
    """

    def __init__(self):
        self.logger = LoggerConfigurator().configure()

    def detect_auth_error(self, stderr_output):
        """
        Verifica si en la salida de error de ngrok se encuentra
        el mensaje de autenticación fallida (ERR_NGROK_108).
        """
        if not stderr_output:
            return False
        if "ERR_NGROK_108" in stderr_output or "authentication failed" in stderr_output:
            self.logger.warning("Detectado error de autenticación en ngrok (ERR_NGROK_108).")
            return True
        return False

    def kill_existing_sessions(self):
        """
        Ejecuta 'ngrok kill' para cerrar cualquier sesión activa.
        Si el proceso persiste, lo fuerza a cerrar en Windows/Linux.
        """
        self.logger.warning("Intentando cerrar sesiones previas de ngrok...")
        try:
            # Ejecutar 'ngrok kill'
            result = subprocess.run(
                ["ngrok", "kill"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.logger.debug("Salida de ngrok kill (stdout): %s", result.stdout.strip())
            self.logger.debug("Salida de ngrok kill (stderr): %s", result.stderr.strip())
            self.logger.info("Sesiones previas de ngrok finalizadas correctamente.")

            # Esperar unos segundos para que la sesión termine
            time.sleep(3)

            # Verificar si el proceso sigue activo y forzar su cierre si es necesario
            if self.is_ngrok_running():
                self.logger.warning("ngrok sigue ejecutándose después de 'ngrok kill'. Forzando cierre...")
                self.force_kill_ngrok()

        except subprocess.CalledProcessError as e:
            self.logger.error("No se pudo cerrar la sesión de ngrok: %s", e)

    def is_ngrok_running(self):
        """
        Verifica si ngrok sigue ejecutándose después de 'ngrok kill'.
        """
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["tasklist"], stdout=subprocess.PIPE, text=True, check=True)
                return "ngrok.exe" in result.stdout
            else:
                result = subprocess.run(["pgrep", "-f", "ngrok"], stdout=subprocess.PIPE, text=True, check=True)
                return bool(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.logger.error("Error al ejecutar el comando para verificar si ngrok sigue ejecutándose: %s", e)
            return False
        except FileNotFoundError as e:
            self.logger.error("El comando para verificar si ngrok sigue ejecutándose no se encontró: %s", e)
            return False

    def force_kill_ngrok(self):
        """
        Fuerza la terminación de ngrok si sigue ejecutándose.
        """
        try:
            if platform.system() == "Windows":
                subprocess.run(
                    ["taskkill", "/F", "/IM", "ngrok.exe"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
        except subprocess.CalledProcessError as e:
            self.logger.error("Error al ejecutar el comando para forzar la terminación de ngrok: %s", e)
        except FileNotFoundError as e:
            self.logger.error("El comando para forzar la terminación de ngrok no se encontró: %s", e)
            self.logger.info("ngrok ha sido cerrado completamente.")
        except subprocess.SubprocessError as e:
            self.logger.error("Error al ejecutar el comando para forzar la terminación de ngrok: %s", e)
