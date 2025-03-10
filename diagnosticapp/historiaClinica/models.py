from django.db import models

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