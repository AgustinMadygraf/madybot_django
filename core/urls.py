"""
Path: core/urls.py
Este archivo se encarga de manejar las rutas de la aplicación core.
"""

from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
]
