# security/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # Opcional: URL para listar intentos sospechosos
    path('suspicious-history/', views.list_suspicious_attempts_view, name='list_suspicious'),
]