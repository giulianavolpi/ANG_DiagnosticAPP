from django.contrib import admin
from .models import Paciente, SimulationStats

admin.site.register(Paciente)
admin.site.register(SimulationStats)