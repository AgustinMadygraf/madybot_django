"""
Path: core/services/data_service.py
Servicio para manejar la lógica principal de recepción y procesamiento de datos.
"""

from marshmallow import ValidationError


class DataService:
    """
    Servicio que encapsula la lógica de validación y generación de respuesta.
    """

    def __init__(self, validator, response_generator, channel, logger):
        self.validator = validator
        self.response_generator = response_generator
        self.channel = channel
        self.logger = logger

    def process_incoming_data(self, json_data: dict) -> str:
        """
        Valida los datos entrantes, obtiene el mensaje y decide si la respuesta
        se genera en streaming o de forma normal.
        Retorna el mensaje de respuesta final para ser renderizado.
        """
        self.logger.info("Validando datos: %s", json_data)
        try:
            valid_data = self.validator.validate(json_data)
        except ValidationError as err:
            self.logger.warning("Error de validación: %s", err.messages)
            raise

        processed_data = self.channel.receive_message(valid_data)
        self.logger.info("Datos procesados desde el canal: %s", processed_data)

        message_text = processed_data.get('message')
        is_stream = processed_data.get('stream', False)

        try:
            if is_stream:
                return self.response_generator.generate_response_streaming(message_text)
            else:
                return self.response_generator.generate_response(message_text)
        except Exception as e:
            self.logger.error("Error procesando la solicitud: %s", e)
            raise
