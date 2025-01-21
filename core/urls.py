from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('receive-data/', views.receive_data, name='receive_data'),
    path('health-check/', views.health_check, name='health_check'),
]
