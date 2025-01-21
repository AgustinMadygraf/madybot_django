"""
Path: core/services/response_generator.py
Este módulo contiene una clase que genera respuestas utilizando un modelo de lenguaje generativo.
"""


class ResponseGenerator:
    """
    Clase que genera respuestas utilizando un modelo de lenguaje generativo.
    """

    def __init__(self, model_config, logger):
        """
        Constructor que recibe una instancia de ModelConfig.
        
        :param model_config: Instancia de la clase ModelConfig que contiene la configuración del modelo generativo.
        :param logger: Logger inyectado.
        """
        self.model_config = model_config
        self.logger = logger
        self.model = self.model_config.model
        self.logger.info("ResponseGenerator inicializado con el modelo configurado.")

    def generate_response(self, message_input: str) -> str:
        """
        Genera una respuesta en base al mensaje de entrada.

        :param message_input: El texto del mensaje de entrada.
        :return: El texto de la respuesta generada por el modelo.
        """
        self.logger.info("Generando respuesta para el mensaje: %s", message_input)
        self._start_chat_session()
        try:
            response = self.chat_session.send_message(message_input)
            return response.text
        except Exception as e:
            self.logger.error("Error durante la generación de la respuesta: %s", e)
            raise

    def _start_chat_session(self):
        """
        Inicia una nueva sesión de chat si no existe una.
        """
        if not hasattr(self, 'chat_session'):
            self.chat_session = self.model.start_chat()
            self.logger.info("Sesión de chat iniciada con el modelo generativo.")
