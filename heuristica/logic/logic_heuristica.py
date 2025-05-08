# heuristica/logic/logic_heuristica.py
import random
import logging
# Importa el modelo donde guarda sus "errores generados" (está en el mismo nivel de app)
from heuristica.models import GeneratedSuspiciousAttempt # Correcto, no cambia

# Importa la señal que va a emitir (está en el mismo nivel de app)
from heuristica.signals import heuristica_checked # Correcto, no cambia


logger = logging.getLogger(__name__)


def check_suspicious(username_attempt, probability=0.2): # Define la probabilidad aquí
    """
    Simula la ejecución de una heurística.
    Con una probabilidad, marca el intento como sospechoso y lo registra en la DB de heuristica.
    Luego, emite una señal indicando el resultado de su chequeo.

    Args:
        username_attempt (str): El nombre de usuario intentado.
        probability (float): Probabilidad (0.0 a 1.0) de marcar como sospechoso.

    Returns:
        bool: True si la heurística lo marcó como sospechoso, False en caso contrario.
              Esta es la información que la app 'login' usará directamente.
    """
    is_suspicious = random.random() < probability
    logger.info(f"HEURISTICA LOGIC: Chequeo para '{username_attempt}', Resultado Sospechoso Simulado: {is_suspicious}")

    if is_suspicious:
        # --- 1. Heuristica registra su "Error Generado" en su propia base de datos ---
        try:
            GeneratedSuspiciousAttempt.objects.create(username_attempted=username_attempt)
            logger.warning(f"HEURISTICA LOGIC: '{username_attempt}' marcado como sospechoso y REGISTRADO (Generado).")
        except Exception as e:
            logger.error(f"HEURISTICA LOGIC: ERROR al registrar intento sospechoso GENERADO para '{username_attempt}': {e}", exc_info=True)

    # --- 2. Heuristica EMITE una señal para notificar sobre su chequeo ---
    # Emite la señal SIN esperar respuesta. El receptor (en reportar) actuará aparte.
    try:
        # Pasamos el resultado de la heurística en la señal para que el receptor lo use
        # 'sender=None' es típico para señales definidas en el módulo signals.py
        heuristica_checked.send(sender=None, username=username_attempt, is_suspicious=is_suspicious)
        logger.info(f"HEURISTICA LOGIC: Señal 'heuristica_checked' emitida para '{username_attempt}' (Sospechoso: {is_suspicious}).")
    except Exception as e:
         logger.error(f"HEURISTICA LOGIC: ERROR al emitir señal 'heuristica_checked' para '{username_attempt}': {e}", exc_info=True)


    # --- 3. Heuristica retorna el resultado booleano directamente a quien la llamó (login) ---
    return is_suspicious