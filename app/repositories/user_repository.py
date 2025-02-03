# app/repositories/user_repository.py

from app.models import User
from app.core.config import db
from utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class UserRepository:
    """
    Repositorio para gestionar la persistencia de usuarios en la base de datos.
    """

    def ensure_user_exists(self, user_id, user_name=None, user_email=None):
        """
        Verifica si un usuario existe en la base de datos. 
        Si no existe, lo inserta con los datos proporcionados.

        :param user_id: Identificador único del usuario.
        :param user_name: (Opcional) Nombre del usuario.
        :param user_email: (Opcional) Correo del usuario.
        :return: El objeto User si ya existía o el nuevo usuario insertado.
        """
        try:
            existing_user = User.query.filter_by(user_id=user_id).first()
            if not existing_user:
                new_user = User(user_id=user_id, user_name=user_name, user_email=user_email)
                db.session.add(new_user)
                db.session.commit()
                logger.info("Usuario %s insertado correctamente.", user_id)
                return new_user
            else:
                logger.info("El usuario %s ya existe.", user_id)
                return existing_user
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            db.session.rollback()
            logger.error("Error eliminando usuario %s: %s", user_id, e)
            return False
