from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.report_stats_view, name='report_stats'),
]