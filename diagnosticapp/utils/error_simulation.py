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
            stats, created = SimulationStats.objects.get_or_create(pk=3)
            SimulationStats.objects.filter(pk=3).update(total_calls=F('total_calls') + 1)

            # Simular el error basado en la probabilidad
            if random.random() < probability:
                logger.warning(f"Simulando error en {func.__name__} con probabilidad {probability} (DB Counter)")
                # Incrementar el contador de errores simulados (atómicamente)
                SimulationStats.objects.filter(pk=3).update(simulated_errors=F('simulated_errors') + 1)
                return None # Retornar None para simular el error
            else:
                # Si no hay error simulado, ejecutar la función original
                return func(*args, **kwargs)
        return wrapper
    return decorator

def get_error_stats():
    """
    Obtiene las estadísticas de errores simulados desde la base de datos.

    Returns:
        dict: Un diccionario con 'total_calls', 'simulated_errors' y 'error_percentage'.
              Retorna 0 para los contadores si no existen.
    """
    try:
        # Intenta obtener la única fila de estadísticas
        stats = SimulationStats.objects.get(pk=3)
        total_calls = stats.total_calls
        simulated_errors = stats.simulated_errors
    except SimulationStats.DoesNotExist:
        # Si la fila aún no existe, los contadores son 0
        total_calls = 0
        simulated_errors = 0

    error_percentage = 0.0
    if total_calls > 0:
        error_percentage = (simulated_errors / total_calls) * 100

    return {
        'total_calls': total_calls,
        'simulated_errors': simulated_errors,
        'error_percentage': round(error_percentage, 2) # Redondear para mostrar
    }

# Opcional: Función para resetear los contadores en la base de datos
def reset_error_stats():
    """
    Reinicia los contadores de errores simulados en la base de datos.
    Elimina la fila para resetear.
    """
    try:
        stats = SimulationStats.objects.get(pk=3)
        stats.delete() # Elimina la fila
        logger.info("Contadores de simulación de errores reiniciados en la base de datos.")
    except SimulationStats.DoesNotExist:
        logger.info("No hay contadores de simulación de errores para reiniciar en la base de datos.")