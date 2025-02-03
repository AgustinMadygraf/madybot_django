"""
Path: app/models.py
"""

from sqlalchemy.sql import func
from app.core.config import db

class User(db.Model):
    "Modelo de datos para la tabla de usuarios."
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    user_name = db.Column(db.String(255), nullable=True)
    user_email = db.Column(db.String(255), nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    screen_resolution = db.Column(db.String(50), nullable=True)
    language = db.Column(db.String(10), nullable=True)
    platform = db.Column(db.String(50), nullable=True)

class Conversation(db.Model):
    "Modelo de datos para la tabla de conversaciones."
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now()) # pylint: disable=not-callable
