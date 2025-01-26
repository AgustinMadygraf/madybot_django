"""
Path: app_flask.py
"""
import sys
from core.config.flask_config import FlaskConfig
from core.data_controller import data_controller

# Inicializar la configuración de Flask
flask_config = FlaskConfig()
app = flask_config.create_app()
config = flask_config.get_config()

# Registrar el blueprint del controlador
try:
    app.register_blueprint(data_controller)
    flask_config.logger.info("Blueprint registrado correctamente.")
except RuntimeError as e:
    flask_config.logger.error("Error al registrar el blueprint: %s", e)
    sys.exit(1)

if __name__ == '__main__':
    try:
        app.run(debug=config['IS_DEVELOPMENT'], host='0.0.0.0', port=5000)
        flask_config.logger.info("Servidor configurado para HTTP.")
    except (OSError, RuntimeError) as e:
        flask_config.logger.error("Error al iniciar el servidor Flask: %s", e)
        sys.exit(1)
