# heuristica/models.py
from django.db import models

class GeneratedSuspiciousAttempt(models.Model):
    """
    Modelo para registrar intentos de login que la heurística marca como sospechosos (Errores Generados).
    """
    # Django añade automáticamente un campo 'id' como Primary Key

    # Nombre de usuario que se intentó usar
    username_attempted = models.CharField(max_length=150, blank=True, null=True)

    # Marca de tiempo de la decisión de la heurística
    timestamp = models.DateTimeField(auto_now_add=True)

    # Opcional: Podrías añadir un campo para la probabilidad usada en la simulación si fuera relevante guardarlo
    # simulated_probability = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


    class Meta:
        # Ordenar por fecha/hora descendente por defecto
        ordering = ['-timestamp']
        verbose_name = "Intento Sospechoso (Generado)"
        verbose_name_plural = "Intentos Sospechosos (Generados)"


    def __str__(self):
        return f"Generado para '{self.username_attempted or 'N/A'}' en {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"