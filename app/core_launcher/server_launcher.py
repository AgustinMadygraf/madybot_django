"""
Path: app/core_launcher/server_launcher.py
Encargado de inicializar y lanzar el servidor Flask.
"""

import sys
from app.core_config.flask_config import FlaskConfig
from app.core_services.data_controller import data_controller

class ServerLauncher:
    def __init__(self):
        """Inicializa la configuración del servidor Flask."""
        self.flask_config = FlaskConfig()
        self.app = self.flask_config.create_app()
        self.config = self.flask_config.get_config()
        self.logger = self.flask_config.logger

    def register_blueprints(self):
        """Registra los blueprints en la aplicación Flask."""
        try:
            self.app.register_blueprint(data_controller)
            self.logger.info("Blueprint registrado correctamente.")
        except RuntimeError as e:
            self.logger.error("Error al registrar el blueprint: %s", e)
            sys.exit(1)

    def run(self):
        """Inicia el servidor Flask."""
        try:
            self.app.run(debug=self.config['IS_DEVELOPMENT'], host='0.0.0.0', port=5000)
            self.logger.info("Servidor iniciado correctamente en HTTP.")
        except (OSError, RuntimeError) as e:
            self.logger.error("Error al iniciar el servidor Flask: %s", e)
            sys.exit(1)

# Si el script se ejecuta directamente, inicia el servidor
if __name__ == '__main__':
    server = ServerLauncher()
    server.register_blueprints()
    server.run()
