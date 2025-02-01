"""
Path: app/core/config.py
"""

import os
import sys
import json
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy  # Importamos SQLAlchemy
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

# Cargar variables desde el archivo .env
load_dotenv()

# Inicializamos SQLAlchemy (se enlazará con la app en create_app)
db = SQLAlchemy()

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

            # Configuración de la base de datos para SQLAlchemy
            config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', '')}@{os.getenv('MYSQL_HOST', 'localhost')}/{os.getenv('MYSQL_DATABASE', 'test')}"
            config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el rastreo de modificaciones para mejorar el rendimiento

            return config
        except FileNotFoundError as e:
            self.logger.error("Error cargando el archivo de configuración: %s", e)
            print("Please create a config.json file with the necessary configuration variables.")
            sys.exit(1)

    def create_app(self):
        """
        Crea y configura la aplicación Flask con SQLAlchemy.
        """
        app = Flask(__name__)
        CORS(app)

        # Cargar configuración en la app Flask
        app.config.update(self.config)

        # Inicializar SQLAlchemy con Flask
        db.init_app(app)

        self.logger.debug("CORS y SQLAlchemy configurados correctamente.")
        return app

    def get_config(self):
        """
        Retorna la configuración cargada desde el archivo JSON.
        """
        return self.config
