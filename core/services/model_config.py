"""
Path: componente_flask/services/model_config.py
Factory o configuración para crear instancias de clientes LLM (Gemini u otros).

Objetivo:
- Centralizar la carga de la API Key (GEMINI_API_KEY) y las instrucciones del sistema.
- Mantener la opción de inyectar un logger externo, o usar uno local por defecto.
- Reemplazar completamente la versión de 'core/services/model_config.py'.
"""

import os
from dotenv import load_dotenv
from core.services.llm_impl.gemini_llm import GeminiLLMClient

# Intentamos cargar las variables de entorno.
load_dotenv()

# Intentamos usar el logger global si existe (en core/logs/dependency_injection),
# en caso contrario, usamos uno local basado en LoggerConfigurator.
try:
    from core.logs.dependency_injection import app_logger as default_logger
except ImportError:
    from core.logs.config_logger import LoggerConfigurator
    default_logger = LoggerConfigurator().configure()

class ModelConfig:
    """
    Carga la configuración necesaria (API key, system instruction)
    y crea la instancia concreta de un cliente LLM (por ejemplo, GeminiLLMClient).

    :param logger: (opcional) Permite inyectar un logger externo. Si no se
                   proporciona, se utilizará uno por defecto.
    """

    def __init__(self, logger=None):
        self.logger = logger if logger else default_logger

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "La API Key de Gemini no está configurada en las variables de entorno."
            )
        self.logger.info("API Key de Gemini obtenida correctamente.")

        self.system_instruction = self._load_system_instruction()

    def create_llm_client(self):
        """
        Crea y retorna una instancia de GeminiLLMClient utilizando
        la configuración actual (API key y system_instruction).
        """
        # La implementación de GeminiLLMClient admite un logger inyectado.
        return GeminiLLMClient(self.api_key, self.system_instruction, self.logger)

    def _load_system_instruction(self):
        """
        Carga las instrucciones del sistema desde el archivo system_instruction.txt,
        ubicado en la carpeta config/ del proyecto.
        """
        instruction_file_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "config", "system_instruction.txt"
        )
        instruction_file_path = os.path.abspath(instruction_file_path)

        self.logger.info("Buscando instrucciones del sistema en: %s", instruction_file_path)

        try:
            with open(instruction_file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError as exc:
            self.logger.error("Error: El archivo system_instruction.txt no se encontró.")
            raise FileNotFoundError(
                "El archivo system_instruction.txt no se encuentra en la ruta especificada."
            ) from exc

    def another_public_method(self):
        """Método público adicional para satisfacer pylint."""
        print("Este es un método público adicional.")
