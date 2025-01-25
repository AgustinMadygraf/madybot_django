"""
Path: core/logs/config_logger.py
Clase LoggerConfigurator mejorada para garantizar una única instancia y configuración consistente.
"""

import logging.config
from typing import Optional
from core.logs.JSON_config_strategy import JSONConfigStrategy
from core.logs.config_strategy import ConfigStrategy

class LoggerConfigurator:
    """Clase singleton para configurar el logger usando una estrategia y filtros dinámicos."""
    _instance = None
    _initialized = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, config_strategy: Optional[ConfigStrategy] = None,
                 default_level: int = logging.INFO):
        """
        Inicializa el configurador del logger (solo una vez).

        Args:
            config_strategy (Optional[ConfigStrategy]): Estrategia de configuración.
            default_level (int): Nivel de log por defecto.
        """
        if not self._initialized:
            self.config_strategy = config_strategy or JSONConfigStrategy()
            self.default_level = default_level
            self.filters = {}
            self._logger = None
            self._initialized = True

    def register_filter(self, name: str, filter_class: type) -> None:
        """
        Registra un filtro dinámicamente.

        Args:
            name (str): Nombre del filtro.
            filter_class (type): Clase del filtro que hereda de logging.Filter.
        """
        if name not in self.filters:
            self.filters[name] = filter_class()

    def configure(self) -> logging.Logger:
        """
        Configura y retorna el logger. Si ya está configurado, retorna la instancia existente.

        Returns:
            logging.Logger: Logger configurado.
        """
        if self._logger is not None:
            return self._logger

        config = self.config_strategy.load_config()

        if config:
            # Registrar filtros dinámicos.
            if 'filters' not in config:
                config['filters'] = {}

            for name, filter_instance in self.filters.items():
                config['filters'][name] = {
                    '()': f"{filter_instance.__class__.__module__}."
                        f"{filter_instance.__class__.__name__}"
                }

            try:
                logging.config.dictConfig(config)
                self._logger = logging.getLogger("app_logger")
            except ValueError as e:  # Error típico en dictConfig.
                logging.error(f"Error en la configuración del logger (dictConfig): {e}")
            except (TypeError, AttributeError, ImportError, KeyError) as e:
                logging.error(f"Error específico al aplicar la configuración: {e}")
                self._use_default_config()
        else:
            self._use_default_config()
        return self._logger
    def _use_default_config(self) -> None:
        """Aplica la configuración por defecto cuando falla la configuración principal."""
        logging.basicConfig(
            level=self.default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._logger = logging.getLogger("app_logger")
        logging.warning("Usando configuración por defecto del logger.")
