# security/signals.py
import django.dispatch
import random
import logging
from .models import SuspiciousLoginAttempt #modelo

logger = logging.getLogger(__name__)

# Define la señal personalizada para intentos de login
# No es necesario poner provide_args si se pasan los argumentos como kwargs en .send()
login_attempt = django.dispatch.Signal()


# --- Receptor de la Señal ---
# Esta función se ejecutará cuando la señal 'login_attempt' sea emitida
# Recibe sender (quien emite la señal, ej: la request) y los argumentos nombrados (username, request)
def check_suspicious_login_receiver(sender, username=None, request=None, **kwargs):
    """
    Receptor de señal para revisar intentos de login emitidos por la vista.
    Simula ser sospechoso con cierta probabilidad y lo registra en la DB.
    """
    # Define la probabilidad de simulación de sospecha
    probability = 0.2 # Ajusta esta probabilidad aquí en el receptor

    is_suspicious = random.random() < probability

    if is_suspicious:
        logger.warning(f"SIGNAL RECEIVER: Ingreso sospechoso SIMULADO para usuario: {username}")
        # Registrar el intento sospechoso en la base de datos
        try:
            SuspiciousLoginAttempt.objects.create(username_attempted=username)
            logger.info(f"SIGNAL RECEIVER: Ingreso sospechoso para '{username}' DETECTADO y REGISTRADO en DB.")
        except Exception as e:
            # Añadir manejo de errores si falla la escritura en DB
            logger.error(f"SIGNAL RECEIVER: ERROR al registrar intento sospechoso para '{username}': {e}")

    