"""
Path: core/logs/logging_setup.py
Configura el logger con rutas de filtros dinámicos.
"""

import logging  # <--- Agregar este import
from logging.config import dictConfig
from core.logs.config_logger import LoggerConfigurator

def configure_logger():
    """
    Configura el logger con los filtros dinámicos.
    """
    configurator = LoggerConfigurator()
    config = configurator.get_config()

    # Asegurar que los filtros tengan sus rutas correctas en la configuración
    if config:
        # Registrar rutas directamente en la configuración de los filtros
        config.setdefault('filters', {}).update({
            'info_error_filter': {
                '()': 'core.logs.info_error_filter.InfoErrorFilter'
            },
            'exclude_http_logs_filter': {
                '()': 'core.logs.exclude_http_logs_filter.ExcludeHTTPLogsFilter'
            },
        })

        dictConfig(config)

    return logging.getLogger('app_logger')


app_logger = configure_logger()
