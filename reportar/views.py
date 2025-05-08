# reportar/views.py
from django.shortcuts import render
# Importa los modelos de AMBAS apps para obtener los contadores
from heuristica.models import GeneratedSuspiciousAttempt # Importa el modelo de heuristica
from .models import DetectedSuspiciousAttempt # Importa el modelo de reportar
import logging

logger = logging.getLogger(__name__)

def report_stats_view(request):
    """
    Vista para mostrar las estadísticas de intentos sospechosos generados vs. detectados.
    """
    # --- 1. Obtener contadores de AMBAS bases de datos (modelos) ---
    total_generated = GeneratedSuspiciousAttempt.objects.count()
    total_detected = DetectedSuspiciousAttempt.objects.count()

    # --- 2. Calcular el porcentaje ---
    # El porcentaje de detectados sobre generados (debería ser 100% si la detección funciona)
    detection_percentage = 0.0
    if total_generated > 0:
         # Calculamos detectados / generados * 100
         detection_percentage = (total_detected / total_generated) * 100

    # --- 3. Preparar el contexto para el template ---
    context = {
        'total_generated': total_generated,
        'total_detected': total_detected,
        'detection_percentage': round(detection_percentage, 2) # Redondeamos para mostrar
    }

    # --- 4. Renderizar el template de estadísticas ---
    return render(request, 'reportar/stats.html', context)