"""
Path: app/components/services/data/user_persistence_service.py
Servicio para gestionar la persistencia de datos de usuarios.
Aplica el SRP, utilizando el patrón de repositorio (REP) para comunicarse con la capa de datos.
"""

from sqlalchemy.exc import DatabaseError, IntegrityError
from app.repositories.user_repository import UserRepository
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class UserPersistenceService:
    " Servicio para gestionar la persistencia de datos de usuarios. "
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save_user(self, user_data: dict):
        """
        Guarda o actualiza los datos del usuario en la base de datos.
        Extrae la información de usuario (incluyendo datos de browser) y la pasa al repositorio.
        """
        try:
            user_id = user_data.get("id")
            user_name = user_data.get("user_name")
            user_email = user_data.get("user_email")
            user_agent = user_data.get("browserData", {}).get("userAgent")
            screen_resolution = user_data.get("browserData", {}).get("screenResolution")
            language = user_data.get("browserData", {}).get("language")
            platform = user_data.get("browserData", {}).get("platform")

            logger.info("Valores a almacenar en la BD (Usuario): ID=%s, Name=%s, Email=%s, UA=%s, SR=%s, Lang=%s, Plat=%s",
                        user_id, user_name, user_email, user_agent, screen_resolution, language, platform)

            return self.user_repository.ensure_user_exists(
                user_id=user_id,
                user_name=user_name,
                user_email=user_email,
                user_agent=user_agent,
                screen_resolution=screen_resolution,
                language=language,
                platform=platform
            )
        except (KeyError, TypeError) as e:
            logger.error("Error al guardar usuario: %s", e)
            return None

    def get_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID.
        """
        try:
            return self.user_repository.get_user_by_id(user_id)
        except (KeyError, TypeError, DatabaseError, IntegrityError) as e:
            logger.error("Error al obtener usuario %s: %s", user_id, e)
            return None
