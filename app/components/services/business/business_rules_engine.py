"""
Path: app/components/services/business/business_rules_engine.py

"""

import json
import re
from difflib import get_close_matches
import pymysql
from Levenshtein import distance as levenshtein_distance
from app.config import FlaskConfig
from app.utils.logging.logger_configurator import LoggerConfigurator

class BusinessRulesEngine:
    """
    Clase que gestiona las reglas de negocio dinámicas para la generación de respuestas.
    Puede obtener reglas desde un archivo JSON o desde MySQL, según la configuración.
    """

    def __init__(self):
        self.logger = LoggerConfigurator().configure()
        self.config = FlaskConfig().get_config()
        self.rule_source = self.config.get("RULE_SOURCE", "json")  # "json" o "mysql"

        if self.rule_source == "json":
            self.rules = self._load_rules_from_json()
        elif self.rule_source == "mysql":
            self.rules = self._load_rules_from_mysql()
        else:
            self.logger.error("RULE_SOURCE no válido en configuración. Debe ser 'json' o 'mysql'.")
            self.rules = {}

    def _load_rules_from_json(self):
        """Carga reglas de negocio desde un archivo JSON."""
        try:
            with open(self.config.get("RULES_JSON_PATH", "config/rules.json"), "r", encoding="utf-8") as file:
                data = json.load(file)

            rules_dict = {}
            for rule in data["rules"]:
                for keyword in rule["keywords"]:
                    rules_dict[keyword.lower()] = rule["response"]

            self.logger.info("Reglas de negocio cargadas desde JSON.")
            return rules_dict
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error("Error cargando reglas desde JSON: %s", e)
            return {}

    def _load_rules_from_mysql(self):
        """Carga reglas de negocio desde MySQL."""
        try:
            db_config = self.config.get("MYSQL_CONFIG")
            connection = pymysql.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT keyword, response FROM business_rules")
                rules = {row["keyword"].lower(): row["response"] for row in cursor.fetchall()}
            connection.close()
            self.logger.info("Reglas de negocio cargadas desde MySQL.")
            return rules
        except (pymysql.MySQLError, pymysql.OperationalError, pymysql.ProgrammingError) as e:
            self.logger.error("Error cargando reglas desde MySQL: %s", e)
            return {}

    def _normalize_text(self, text: str) -> str:
        """
        Normaliza el texto:
        - Convierte a minúsculas
        - Elimina signos de puntuación
        - Reduce repeticiones de letras (ej. "holaaa" → "hola")
        """
        text = text.lower()
        text = re.sub(r"[^a-záéíóúüñ\s]", "", text)  # Quitar signos de puntuación
        text = re.sub(r"(.)\1{2,}", r"\1", text)  # Reducir repeticiones excesivas de letras
        return text.strip()

    def get_response(self, message_input: str):
        """
        Busca una respuesta en las reglas de negocio con:
        - Coincidencia exacta
        - Búsqueda aproximada con `difflib`
        - Distancia de Levenshtein para errores tipográficos
        """
        message_input = self._normalize_text(message_input)

        # Búsqueda exacta
        if message_input in self.rules:
            return self.rules[message_input]

        # Búsqueda aproximada con `difflib`
        close_matches = get_close_matches(message_input, self.rules.keys(), n=1, cutoff=0.7)
        if close_matches:
            self.logger.info("Match aproximado encontrado: %s", close_matches[0])
            return self.rules[close_matches[0]]

        # Comparación con distancia de Levenshtein
        best_match = None
        min_distance = float("inf")
        for keyword in self.rules.keys():
            distance = levenshtein_distance(message_input, keyword)
            if distance < min_distance and distance <= 2:  # Solo aceptar si hay 2 o menos diferencias
                min_distance = distance
                best_match = keyword

        if best_match:
            self.logger.info("Match basado en Levenshtein encontrado: %s", best_match)
            return self.rules[best_match]

        return None  # No se encontró una respuesta en las reglas
