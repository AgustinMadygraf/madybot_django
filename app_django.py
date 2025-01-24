"""
Path: app_django.py

"""

import os
import sys
from dotenv import load_dotenv
from django.core.management import execute_from_command_line
from core.logs.config_logger import LoggerConfigurator

def main():
    "Entrypoint para iniciar el servidor Django."
    logger = LoggerConfigurator().configure()
    try:
        if not load_dotenv():
            raise FileNotFoundError(".env file not found")
        logger.debug(".env file cargado correctamente")
    except FileNotFoundError as e:
        logger.error("Error loading .env file: %s", e)
        print("Por favor, crea un .env con las variables necesarias.")
        sys.exit(1)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'madybot_django.settings')
    # Argumentos por defecto para runserver
    sys.argv = ['manage.py', 'runserver']
    logger.debug("Iniciando servidor Django")
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
