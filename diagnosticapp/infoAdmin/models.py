from django.db import models
import time
import random

# Create your models here.
class infoAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    
    def __str__(self):
        return '{}'.format(self.nombre)
    
    #Simulador de acceso a información de administrador
    def validar_acceso(self):
        time.sleep(random.uniform(0.05, 0.15))  
        return self.tiene_acceso