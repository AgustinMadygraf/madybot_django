"""
Path: app/core/config.py
"""

import os
import sys
import json
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

# Cargar variables desde el archivo .env
load_dotenv()

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
        Carga la configuración desde el archivo JSON y complementa con variables de entorno.
        """
        try:
            self.logger.debug("Intentando cargar el archivo %s", self.config_path)
            with open(self.config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
            self.logger.debug("Archivo de configuración cargado correctamente.")

            # Sobrescribir valores de configuración con variables de entorno si están definidas
            config['mysql'] = {
                'host': os.getenv('MYSQL_HOST', config.get('mysql', {}).get('host', 'localhost')),
                'user': os.getenv('MYSQL_USER', config.get('mysql', {}).get('user', 'root')),
                'password': os.getenv('MYSQL_PASSWORD', config.get('mysql', {}).get('password', '')),
                'database': os.getenv('MYSQL_DATABASE', config.get('mysql', {}).get('database', 'test')),
            }

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
