from django.db import models
import time
import random

# Create your models here.
class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    genero = models.CharField(max_length=50)
    medico = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre)
    
    
class HistoriaClinica(models.Model):
    paciente_id = models.CharField(max_length=100)
    es_menor_edad = models.BooleanField(default=False)
    existe = models.BooleanField(default=True)

    #Simulador de consulta de historia clínica
    def consultar_historia(self):
        time.sleep(random.uniform(0.05, 0.2))  
        if self.existe and self.es_menor_edad:
            return {"paciente_id": self.paciente_id, "datos": "Información simulada"}
        return None
