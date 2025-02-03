"""
Path: app/repositories/user_repository.py

"""

from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.core.config import db
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class UserRepository:
    """
    Repositorio para gestionar la persistencia de usuarios en la base de datos.
    """

    def ensure_user_exists(self, user_id, user_name=None, user_email=None, user_agent=None,
                        screen_resolution=None, language=None, platform=None):
        """
        Verifica si un usuario existe en la base de datos. 
        Si no existe, lo inserta con los datos proporcionados; si ya existe, se actualizan
        los campos adicionales si se proporcionan nuevos valores.
        
        :param user_id: Identificador único del usuario.
        :param user_name: (Opcional) Nombre del usuario.
        :param user_email: (Opcional) Correo del usuario.
        :param user_agent: (Opcional) User-Agent del navegador.
        :param screen_resolution: (Opcional) Resolución de pantalla.
        :param language: (Opcional) Idioma.
        :param platform: (Opcional) Plataforma.
        :return: El objeto User insertado o actualizado.
        """
        try:
            existing_user = User.query.filter_by(user_id=user_id).first()
            if not existing_user:
                new_user = User(
                    user_id=user_id,
                    user_name=user_name,
                    user_email=user_email,
                    user_agent=user_agent,
                    screen_resolution=screen_resolution,
                    language=language,
                    platform=platform
                )
                db.session.add(new_user)
                db.session.commit()
                logger.info("Usuario %s insertado correctamente.", user_id)
                return new_user
            else:
                updated = False
                if user_name is not None and existing_user.user_name != user_name:
                    existing_user.user_name = user_name
                    updated = True
                if user_email is not None and existing_user.user_email != user_email:
                    existing_user.user_email = user_email
                    updated = True
                if user_agent is not None and existing_user.user_agent != user_agent:
                    existing_user.user_agent = user_agent
                    updated = True
                if screen_resolution is not None and existing_user.screen_resolution != screen_resolution:
                    existing_user.screen_resolution = screen_resolution
                    updated = True
                if language is not None and existing_user.language != language:
                    existing_user.language = language
                    updated = True
                if platform is not None and existing_user.platform != platform:
                    existing_user.platform = platform
                    updated = True
                if updated:
                    db.session.commit()
                logger.info("El usuario %s ya existe y se actualizó la información.", user_id)
                return existing_user
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Error en ensure_user_exists: %s", e)
            return None

    def get_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID único.

        :param user_id: Identificador del usuario.
        :return: Objeto User o None si no se encuentra.
        """
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                return user
            else:
                logger.warning("Usuario %s no encontrado.", user_id)
                return None
        except SQLAlchemyError as e:
            logger.error("Error obteniendo usuario %s: %s", user_id, e)
            return None

    def update_user(self, user_id, user_name=None, user_email=None):
        """
        Actualiza los datos de un usuario en la base de datos.

        :param user_id: Identificador único del usuario.
        :param user_name: (Opcional) Nuevo nombre del usuario.
        :param user_email: (Opcional) Nuevo correo del usuario.
        :return: El objeto User actualizado o None en caso de error.
        """
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                if user_name:
                    user.user_name = user_name
                if user_email:
                    user.user_email = user_email
                db.session.commit()
                logger.info("Usuario %s actualizado correctamente.", user_id)
                return user
            else:
                logger.warning("No se encontró el usuario %s para actualizar.", user_id)
                return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Error actualizando usuario %s: %s", user_id, e)
            return None

    def delete_user(self, user_id):
        """
        Elimina un usuario de la base de datos.

        :param user_id: Identificador único del usuario a eliminar.
        :return: True si se eliminó correctamente, False en caso de error.
        """
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                logger.info("Usuario %s eliminado correctamente.", user_id)
                return True
            else:
                logger.warning("No se encontró el usuario %s para eliminar.", user_id)
                return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Error eliminando usuario %s: %s", user_id, e)
            return False
