# app/models.py
from app.core.config import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    user_name = db.Column(db.String(255), nullable=True)
    user_email = db.Column(db.String(255), nullable=True)
    # Puedes agregar otros campos que consideres necesarios

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
