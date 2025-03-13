from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes_list, name='pacientes_list'),
]
