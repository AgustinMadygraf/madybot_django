"""
Path: core/views.py
Este archivo se encarga de manejar las vistas de la aplicación core.
"""

from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola, Django está funcionando!")
