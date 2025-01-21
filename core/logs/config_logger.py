"""
Path: core/logs/config_logger.py
Clase LoggerConfigurator mejorada para soportar filtros dinámicos.
"""

import os
import json
from abc import ABC, abstractmethod
from logging import Filter

class ConfigStrategy(ABC):
    """Clase base para las estrategias de configuración del logger."""

    @abstractmethod
    def load_config(self):
        """Método que debe implementarse para cargar la configuración."""
        pass


class JSONConfigStrategy(ConfigStrategy):
    """Estrategia para cargar la configuración desde un archivo JSON."""

    def __init__(self, config_path='core/logs/logging.json', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Carga la configuración desde un archivo JSON o ruta especificada en una variable de entorno."""
        path = os.getenv(self.env_key, self.config_path)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None


class LoggerConfigurator:
    """
    Clase que utiliza una estrategia de configuración para
    cargar filtros y el diccionario de configuración del logger.
    """

    def __init__(self, config_strategy: ConfigStrategy = None):
        self.config_strategy = config_strategy or JSONConfigStrategy()
        self.filters = {}

    def get_config(self):
        """Retorna la configuración del logger usando la estrategia asignada."""
        return self.config_strategy.load_config()

    def register_filter(self, name: str, filter_class: type[Filter]):
        """
        Registra un filtro dinámicamente.

        :param name: Nombre del filtro.
        :param filter_class: Clase del filtro que hereda de logging.Filter.
        """
        self.filters[name] = filter_class()

    def get_filters(self):
        """
        Retorna los filtros registrados.

        :return: Diccionario con filtros configurados.
        """
        return self.filters
