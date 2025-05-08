# security/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import logging
from .models import SuspiciousLoginAttempt # Importamos el modelo que creamos

logger = logging.getLogger(__name__)

# --- Lógica de Simulación de Ingreso Sospechoso ---
def check_suspicious_login(username_attempt, probability=0.2): # Ajusta la probabilidad aquí (ej: 20%)
    """
    Simula la revisión de un intento de login.
    Con una probabilidad, lo marca como sospechoso y lo registra.

    Args:
        username_attempt (str): El nombre de usuario intentado.
        probability (float): Probabilidad (0.0 a 1.0) de marcar como sospechoso.

    Returns:
        bool: True si el intento fue marcado y registrado como sospechoso, False en caso contrario.
    """
    is_suspicious = random.random() < probability

    if is_suspicious:
        logger.warning(f"Simulando ingreso sospechoso para usuario: {username_attempt}")
        # Registrar el intento sospechoso en la base de datos
        # Esto es nuestra "detección exitosa del 100%" del evento simulado
        SuspiciousLoginAttempt.objects.create(username_attempted=username_attempt)
        return True # Indicamos que fue sospechoso y detectado
    else:
        logger.info(f"Ingreso simulado normal para usuario: {username_attempt}")
        return False # Indicamos que no fue marcado como sospechoso

# --- Vista de Login ---
def login_view(request):
    message = None
    username_attempted = None
    is_suspicious = False

    if request.method == 'POST':
        username_attempted = request.POST.get('username')

        if not username_attempted:
            message = "Por favor, ingrese un nombre de usuario."
        else:
            # Llamamos a nuestra lógica de simulación
            is_suspicious = check_suspicious_login(username_attempted)

            if is_suspicious:
                message = f"¡Ingreso para '{username_attempted}' marcado como SOSPECHOSO y DETECTADO!"
                # Aquí podrías redirigir a una página de "Acceso Denegado" o similar
                # return render(request, 'security/access_denied.html', {'message': message})
            else:
                message = f"Ingreso para '{username_attempted}' simulado como normal. (No sospechoso)."
                # Aquí podrías simular un login exitoso y redirigir al inicio, por ejemplo:
                # return redirect('/') # Redirige a la página principal

    # Si es GET o después de procesar POST (a menos que se redirija)
    # Prepara el contexto para el template
    context = {
        'message': message,
        'username_attempted': username_attempted,
        'is_suspicious': is_suspicious,
        # Opcional: pasar aquí el total de intentos sospechosos detectados
        'total_suspicious_detected': SuspiciousLoginAttempt.objects.count()
    }

    return render(request, 'security/login.html', context)


# --- Opcional: Vista para listar todos los intentos sospechosos detectados ---
def list_suspicious_attempts_view(request):
    attempts = SuspiciousLoginAttempt.objects.all()
    context = {
        'suspicious_attempts': attempts,
        'total_suspicious_detected': attempts.count()
    }
    return render(request, 'security/list_suspicious.html', context)