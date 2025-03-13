from django.db import models
from infoAdmin.models import Medico

class Paciente(models.Model):
    medicos = models.ManyToManyField(Medico)
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    edad = models.IntegerField()