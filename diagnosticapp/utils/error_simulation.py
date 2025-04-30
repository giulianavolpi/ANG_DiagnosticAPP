# tu_app/utils/error_simulation.py
import random
import functools
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

# Define las claves para la caché
CACHE_KEY_TOTAL_CALLS = 'error_simulation:total_calls'
CACHE_KEY_SIMULATED_ERRORS = 'error_simulation:simulated_errors'

def simulate_error_probability(probability=0.1):
    """
    Decorador que simula un error (retornando None) con una cierta probabilidad.
    También cuenta el total de llamadas y errores simulados usando la caché.

    Args:
        probability (float): La probabilidad (entre 0.0 y 1.0) de que ocurra el error simulado.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Incrementar el contador total de llamadas ANTES de la simulación
            try:
                # cache.incr es atómico, bueno para concurrencia básica
                cache.incr(CACHE_KEY_TOTAL_CALLS)
            except ValueError:
                 # La clave no existe o no es un entero, inicializar
                 cache.set(CACHE_KEY_TOTAL_CALLS, 1, timeout=None) # timeout=None significa nunca expira por tiempo

            # Simular el error basado en la probabilidad
            if random.random() < probability:
                logger.warning(f"Simulando error en {func.__name__} con probabilidad {probability}")
                # Incrementar el contador de errores simulados
                try:
                    cache.incr(CACHE_KEY_SIMULATED_ERRORS)
                except ValueError:
                     # La clave no existe o no es un entero, inicializar
                     cache.set(CACHE_KEY_SIMULATED_ERRORS, 1, timeout=None) # timeout=None

                return None # Retornar None para simular el error
            else:
                # Si no hay error simulado, ejecutar la función original
                return func(*args, **kwargs)
        return wrapper
    return decorator

def get_error_stats():
    """
    Obtiene las estadísticas de errores simulados desde la caché.

    Returns:
        dict: Un diccionario con 'total_calls', 'simulated_errors' y 'error_percentage'.
              Retorna 0 para los contadores si no existen.
    """
    # Usamos get para obtener los valores, con 0 como valor por defecto si no existen
    total_calls = cache.get(CACHE_KEY_TOTAL_CALLS, 0)
    simulated_errors = cache.get(CACHE_KEY_SIMULATED_ERRORS, 0)

    error_percentage = 0.0 # Usar float
    if total_calls > 0:
        error_percentage = (simulated_errors / total_calls) * 100

    return {
        'total_calls': total_calls,
        'simulated_errors': simulated_errors,
        'error_percentage': round(error_percentage, 2) # Redondear para mostrar
    }

# Opcional: Función para resetear los contadores, útil para pruebas.
def reset_error_stats():
    """
    Reinicia los contadores de errores simulados en la caché.
    """
    cache.delete(CACHE_KEY_TOTAL_CALLS)
    cache.delete(CACHE_KEY_SIMULATED_ERRORS)
    logger.info("Contadores de simulación de errores reiniciados.")