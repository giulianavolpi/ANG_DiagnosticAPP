# reportar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapeamos la URL '/stats/' a la vista report_stats_view
    path('stats/', views.report_stats_view, name='report_stats'),
]