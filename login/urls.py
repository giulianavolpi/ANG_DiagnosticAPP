# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapeamos la URL '/login/' DENTRO de la app 'login' a la vista login_view.
    # Con el include en diagnosticapp/urls.py, la URL final será /login/.
    path('login/', views.login_view, name='login'),

    # La línea original path('', views.login_view, name='login') ya no se usa
    # si quieres que la URL sea /login/.
]