from django.db import models

class DetectedSuspiciousAttempt(models.Model):
    """
    Modelo para registrar intentos de login que la app 'reportar' detecta (al escuchar la señal).
    (Errores Detectados).
    """
    # Django añade automáticamente un campo 'id' como Primary Key

    # Nombre de usuario que se intentó usar (copiado de la señal)
    username_attempted = models.CharField(max_length=150, blank=True, null=True)

    # Marca de tiempo de la detección (cuando el receptor guarda el registro)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ordenar por fecha/hora descendente por defecto
        ordering = ['-timestamp']
        verbose_name = "Intento Sospechoso (Detectado)"
        verbose_name_plural = "Intentos Sospechosos (Detectados)"


    def __str__(self):
        return f"Detectado para '{self.username_attempted or 'N/A'}' en {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"