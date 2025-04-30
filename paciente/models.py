from django.db import models
from infoAdmin.models import Medico

class Paciente(models.Model):
    medicos = models.ManyToManyField(Medico)
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    edad = models.IntegerField()

#Nuevo para guardar errores en la db
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
