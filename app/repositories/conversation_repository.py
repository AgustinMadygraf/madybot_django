"""
Módulo de gestión de conversaciones en la base de datos.
Ubicación: app/repositories/conversation_repository.py
"""

from mysql.connector import Error
from app.infrastructure.database_connection import DatabaseConnection
from app.repositories.user_repository import UserRepository
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class ConversationRepository:
    "Gestión de conversaciones en la base de datos."

    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()
        self.user_repo = UserRepository()
        self._create_conversations_table()

    def _create_conversations_table(self):
        "Crea la tabla `conversations` si no existe."
        try:
            cursor = self.connection.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS conversations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            """
            cursor.execute(query)
            self.connection.commit()
            logger.info("Tabla 'conversations' verificada o creada correctamente.")
            cursor.close()
        except Error as e:
            logger.error("Error al crear/verificar la tabla 'conversations': %s", e)

    def insert_conversation(self, user_id, message, response):
        "Guarda una conversación en la base de datos."
        try:
            cursor = self.connection.cursor()

            # Asegurar que el usuario existe antes de insertar la conversación
            self.user_repo.ensure_user_exists(user_id)

            cursor.execute(
                "INSERT INTO conversations (user_id, message, response) VALUES (%s, %s, %s)",
                (user_id, message, response)
            )
            self.connection.commit()
            cursor.close()
            logger.info("Conversación almacenada correctamente para user_id: %s", user_id)
        except Error as e:
            logger.error("Error insertando conversación: %s", e)
