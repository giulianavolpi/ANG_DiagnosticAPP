# security/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import logging
from .models import SuspiciousLoginAttempt
from .signals import login_attempt
# Importa reverse si no lo has hecho para las URLs
from django.urls import reverse # Necesario si usas reverse

logger = logging.getLogger(__name__)

# ... tu función check_suspicious_login_receiver (receptor de señal) ...


# --- Vista de Login (Modificada para Sesión) ---
def login_view(request):
    message = None
    username_attempted = None
    # is_suspicious_result ya no se calcula ni se usa directamente aquí para el mensaje principal

    if request.method == 'POST':
        username_attempted = request.POST.get('username')

        if not username_attempted:
            message = "Por favor, ingrese un nombre de usuario."
        else:
            # --- Emitir la Señal (la lógica de sospecha ocurre en el receptor) ---
            login_attempt.send(sender=request, username=username_attempted, request=request)
            logger.info(f"VIEW: Señal 'login_attempt' emitida para usuario: {username_attempted}")
            # --- Fin Emitir Señal ---

            # --- Simulación del Resultado del Login Principal ---
            # Esta lógica decide si el login parece "exitoso" o "fallido" para el usuario.
            if random.random() < 0.8: # Ej: 80% de probabilidad de "login principal exitoso" simulado
                login_successful_simulated = True
                message = f"Login para '{username_attempted}' simulado como exitoso."
                logger.info(f"VIEW: Login principal simulado exitoso para usuario: {username_attempted} -> Marcando sesión y redirigiendo.")

                # >>> Marcar al usuario como "autenticado" en la sesión <<<
                request.session['simulated_authenticated'] = True
                request.session['simulated_username'] = username_attempted # Opcional: guardar el nombre de usuario simulado

                # Redirige a la página principal si el login principal fue "exitoso" simulado
                return redirect('/') # O reverse('nombre_de_tu_url_principal')

            else:
                # Simulación de "login principal fallido"
                login_successful_simulated = False
                message = f"Login para '{username_attempted}' simulado como FALLIDO (credenciales inválidas)."
                logger.info(f"VIEW: Login principal simulado fallido para usuario: {username_attempted} -> Mostrando mensaje de error.")
                # >>> Opcional: Asegurarse de que la sesión no marque como autenticado <<<
                request.session['simulated_authenticated'] = False # O simplemente no hacer nada, el False por defecto al leer es suficiente
                if 'simulated_username' in request.session:
                     del request.session['simulated_username']

        # Prepara el contexto (si es GET o si es POST y el login falló simulado)
        context = {
            'message': message,
            'username_attempted': username_attempted,
            'total_suspicious_detected': SuspiciousLoginAttempt.objects.count()
        }

        return render(request, 'security/login.html', context)


# ... tu vista list_suspicious_attempts_view ...
def list_suspicious_attempts_view(request):
    # ... (código igual) ...
    attempts = SuspiciousLoginAttempt.objects.all()
    context = {
        'suspicious_attempts': attempts,
        'total_suspicious_detected': attempts.count()
    }
    return render(request, 'security/list_suspicious.html', context)