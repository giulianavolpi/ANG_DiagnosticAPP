# tu_app/utils/error_simulation.py
import random
import functools
# Importa el modelo de la base de datos
from paciente.models import SimulationStats # Ajusta la ruta de importación
# Importa F para actualizaciones atómicas
from django.db.models import F
from django.db import transaction # Para asegurar atomicidad si es necesario, aunque F() ya ayuda
import logging

logger = logging.getLogger(__name__)

# Ya no necesitamos las claves de caché

def simulate_error_probability(probability=0.1):
    """
    Decorador que simula un error (retornando None) con una cierta probabilidad.
    Cuenta el total de llamadas y errores simulados usando la base de datos.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Incrementar el contador total de llamadas usando la base de datos (atómicamente)
            # Usamos get_or_create para asegurarnos de que la fila existe
            stats, created = SimulationStats.objects.get_or_create(pk=1)
            SimulationStats.objects.filter(pk=1).update(total_calls=F('total_calls') + 1)

            # Simular el error basado en la probabilidad
            if random.random() < probability:
                logger.warning(f"Simulando error en {func.__name__} con probabilidad {probability} (DB Counter)")
                # Incrementar el contador de errores simulados (atómicamente)
                SimulationStats.objects.filter(pk=1).update(simulated_errors=F('simulated_errors') + 1)
                return None # Retornar None para simular el error
            else:
                # Si no hay error simulado, ejecutar la función original
                return func(*args, **kwargs)
        return wrapper
    return decorator

def get_error_stats(param_pk):
    try:
        stats = SimulationStats.objects.get(pk=param_pk)
        simulated_errors = stats.simulated_errors
    except SimulationStats.DoesNotExist:
        simulated_errors = 0

    return simulated_errors

# Opcional: Función para resetear los contadores en la base de datos
def reset_error_stats():
    """
    Reinicia los contadores de errores simulados en la base de datos.
    Elimina la fila para resetear.
    """
    try:
        stats = SimulationStats.objects.get(pk=1)
        stats.delete() # Elimina la fila
        logger.info("Contadores de simulación de errores reiniciados en la base de datos.")
    except SimulationStats.DoesNotExist:
        logger.info("No hay contadores de simulación de errores para reiniciar en la base de datos.")