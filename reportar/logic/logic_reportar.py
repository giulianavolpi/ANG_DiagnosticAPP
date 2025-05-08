# reportar/receivers.py
# Importa la señal de la app heuristica que vamos a escuchar
from heuristica.signals import heuristica_checked
# Importa el modelo donde vamos a guardar las detecciones
from ..models import DetectedSuspiciousAttempt
import logging

logger = logging.getLogger(__name__)

# --- Receptor para la señal heuristica_checked ---
# Esta función se activará cuando la señal heuristica_checked sea emitida.
# Recibe el sender y los argumentos que la señal envió (username, is_suspicious).
def report_suspicious_receiver(sender, username=None, is_suspicious=None, **kwargs):
    """
    Receptor de señal para la señal heuristica_checked.
    Si la heurística marcó el intento como sospechoso, lo registra
    en la base de datos de 'reportar' como un error detectado.
    """
    logger.info(f"REPORTAR RECEIVER: Señal 'heuristica_checked' recibida para '{username}' (Sospechoso según heuristica: {is_suspicious}).")

    # --- 1. Reportar "detecta" el error si la heurística dijo que era sospechoso ---
    if is_suspicious:
        # --- 2. Reportar registra su "Error Detectado" en su propia base de datos ---
        try:
            DetectedSuspiciousAttempt.objects.create(username_attempted=username)
            logger.warning(f"REPORTAR RECEIVER: '{username}' marcado como sospechoso por heuristica y REGISTRADO (Detectado).")
        except Exception as e:
            logger.error(f"REPORTAR RECEIVER: ERROR al registrar intento sospechoso DETECTADO para '{username}': {e}", exc_info=True)

    # Los receptores normalmente no retornan valores que se utilicen.
    # Su propósito es realizar acciones secundarias.

# NOTA: La conexión de este receptor a la señal 'heuristica_checked'
# se hará en el apps.py de la app 'reportar'.