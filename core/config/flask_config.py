"""
Path: core/config/flask_config.py

"""

import json
import sys
from flask import Flask
from flask_cors import CORS
from core.logs.logger_configurator import LoggerConfigurator


class FlaskConfig:
    """
    Clase para manejar la configuración de la aplicación Flask.
    """
    def __init__(self, config_path='config/config.json'):
        self.logger = LoggerConfigurator().configure()
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """
        Carga el archivo de configuración JSON.
        """
        try:
            self.logger.debug("Intentando cargar el archivo %s", self.config_path)
            with open(self.config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
            self.logger.debug("Archivo de configuración cargado correctamente.")
            return config
        except FileNotFoundError as e:
            self.logger.error("Error cargando el archivo de configuración: %s", e)
            print("Please create a config.json file with the necessary configuration variables.")
            sys.exit(1)

    def create_app(self):
        """
        Crea y configura la aplicación Flask.
        """
        app = Flask(__name__)
        CORS(app)
        self.logger.debug("CORS configurado correctamente.")
        return app

    def get_config(self):
        """
        Retorna la configuración cargada desde el archivo JSON.
        """
        return self.config
