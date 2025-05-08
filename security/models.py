# security/models.py
from django.db import models

class SuspiciousLoginAttempt(models.Model):
    """
    Modelo para registrar intentos de login simulados como sospechosos.
    """
    # Django añade automáticamente un campo 'id' como Primary Key

    # Nombre de usuario que se intentó usar
    username_attempted = models.CharField(max_length=150, blank=True, null=True)

    # Marca de tiempo del intento
    timestamp = models.DateTimeField(auto_now_add=True) # auto_now_add=True registra la fecha/hora de creación

    # Opcional: Podrías añadir un campo para la probabilidad usada en la simulación si fuera relevante guardarlo
    # simulated_probability = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


    class Meta:
        # Ordenar por fecha/hora descendente por defecto
        ordering = ['-timestamp']
        verbose_name = "Intento de Login Sospechoso"
        verbose_name_plural = "Intentos de Login Sospechosos"


    def __str__(self):
        # Representación legible del objeto
        return f"Intento sospechoso para '{self.username_attempted or 'N/A'}' en {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"