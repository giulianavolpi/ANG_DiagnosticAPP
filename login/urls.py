# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapeamos la URL '/login/' a la vista login_view
    # Le damos el nombre 'login' para poder referenciarla fácilmente (ej: en redirecciones)
    path('', views.login_view, name='login'),
    # Si quieres que sea en el path '/login/', la linea seria:
    # path('login/', views.login_view, name='login'),
]