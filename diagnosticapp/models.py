# Para tener memoria compartida de los errores 
# diagnosticapp/models.py
from django.db import models

# Modelo para almacenar las estadísticas de simulación de errores
class SimulationStats(models.Model):
    # Usamos una clave primaria fija (ej: 1) para asegurar que solo haya una fila
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    total_calls = models.PositiveIntegerField(default=0)
    simulated_errors = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Estadísticas de Simulación"
        verbose_name_plural = "Estadísticas de Simulación"

    def __str__(self):
        return "Estadísticas de Simulación de Errores"

# Asegúrate de ejecutar:
# python manage.py makemigrations diagnosticapp
# python manage.py migrate