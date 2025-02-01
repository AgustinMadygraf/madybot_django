"""
Módulo de gestión de usuarios en la base de datos.
Ubicación: app/repositories/user_repository.py
"""

from mysql.connector import Error
from app.infrastructure.database_connection import DatabaseConnection
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class UserRepository:
    "Gestión de usuarios en la base de datos."

    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()
        self._create_users_table()

    def _create_users_table(self):
        "Crea la tabla `users` si no existe."
        try:
            cursor = self.connection.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) UNIQUE NOT NULL,
                user_name VARCHAR(255),
                user_email VARCHAR(255)
            )
            """
            cursor.execute(query)
            self.connection.commit()
            logger.info("Tabla 'users' verificada o creada correctamente.")
            cursor.close()
        except Error as e:
            logger.error("Error al crear/verificar la tabla 'users': %s", e)

    def ensure_user_exists(self, user_id, user_name=None, user_email=None):
        "Verifica si un usuario existe en la BD y lo inserta si no está."
        try:
            cursor = self.connection.cursor()

            # Verificar si el usuario ya existe
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                cursor.execute(
                    "INSERT INTO users (user_id, user_name, user_email) VALUES (%s, %s, %s)",
                    (user_id, user_name, user_email)
                )
                self.connection.commit()
                logger.info("Usuario %s insertado correctamente.", user_id)
            cursor.close()
        except Error as e:
            logger.error("Error en ensure_user_exists: %s", e)
