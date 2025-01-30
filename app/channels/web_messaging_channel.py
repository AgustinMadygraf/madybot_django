"""
Path: app/channels/web_messaging_channel.py

"""

from app.channels.imessaging_channel import IMessagingChannel
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class WebMessagingChannel(IMessagingChannel):
    "Esta clase implementa el canal de mensajería para la interfaz web."
    def send_message(self, msg: str, chat_id: str = None) -> None:
        logger.info("Mensaje enviado al usuario web: %s", msg)

    def receive_message(self, payload: dict) -> dict:
        logger.info("Mensaje recibido desde la interfaz web: %s", payload)
        return {
            "message": payload.get('prompt_user'),
            "stream": payload.get('stream', False)
        }
