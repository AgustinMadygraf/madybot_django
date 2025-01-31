"""
Path: app/utils/mysql_connector.py
Este script se encarga de manejar la conexión a la base de datos MySQL.
"""

import mysql.connector
from mysql.connector import Error
from app.config import FlaskConfig

class MySQLConnector:
    "Maneja la conexión a la base de datos MySQL."
    def __init__(self):
        self.connection = None  # Ensure connection is always defined
        config = FlaskConfig().mysql_config
        try:
            self.connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"Connected to MySQL Server version {db_info}")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def execute_query(self, query, params=None):
        "Ejecuta una consulta en la base de datos."
        if self.connection is None or not self.connection.is_connected():
            print("No connection to MySQL.")
            return None
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def fetch_query(self, query, params=None):
        "Obtiene los resultados de una consulta en la base de datos."
        if self.connection is None or not self.connection.is_connected():
            print("No connection to MySQL.")
            return None
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching query: {e}")
            return None
