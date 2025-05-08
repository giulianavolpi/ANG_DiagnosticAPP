# security/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random # Todavía necesario para simular el resultado del login principal
import logging
# Ya NO necesitamos importar SuspiciousLoginAttempt
# Ya NO necesitamos importar check_suspicious_login
# Importa la señal que creaste
from .signals import login_attempt # <<< Importa la señal

# Importa el modelo SOLO para obtener el contador total para la vista
from .models import SuspiciousLoginAttempt # <<< Importa el modelo solo para el contador

logger = logging.getLogger(__name__)

# La función check_suspicious_login YA NO ESTA AQUI. Esta en signals.py.


# --- Vista de Login (Simplificada) ---
def login_view(request):
    message = None
    username_attempted = None
    # is_suspicious_result ya no se calcula ni se usa directamente aquí para el mensaje principal

    if request.method == 'POST':
        username_attempted = request.POST.get('username')

        if not username_attempted:
            message = "Por favor, ingrese un nombre de usuario."
        else:
            # --- ¡Emitir la Señal de Intento de Login! ---
            # Esta es la acción principal relacionada con el intento.
            # Los receptores (en signals.py) se encargarán de la lógica secundaria (sospecha, guardar).
            login_attempt.send(sender=request, username=username_attempted, request=request)
            logger.info(f"VIEW: Señal 'login_attempt' emitida para usuario: {username_attempted}")
            # --- Fin Emitir Señal ---

            # --- Simulación del Resultado del Login Principal (Separado de la sospecha) ---
            # Esta lógica decide si el login parece "exitoso" o "fallido" desde la perspectiva del usuario,
            # independientemente de si fue marcado como sospechoso en segundo plano por la señal.
            if random.random() < 0.8: # Ej: 80% de probabilidad de "login principal exitoso" simulado
                login_successful_simulated = True
                message = f"Login para '{username_attempted}' simulado como exitoso."
                logger.info(f"VIEW: Login principal simulado exitoso para usuario: {username_attempted} -> Redirigiendo.")
                # Redirige a la página principal si el login principal fue "exitoso" simulado
                return redirect('/') # Redirige al path raíz

            else:
                # Simulación de "login principal fallido"
                login_successful_simulated = False
                message = f"Login para '{username_attempted}' simulado como FALLIDO (credenciales inválidas)."
                logger.info(f"VIEW: Login principal simulado fallido para usuario: {username_attempted} -> Mostrando mensaje de error.")
                # Nos quedamos en la página de login si el login principal fue "fallido" simulado

    # Prepara el contexto para el template (se usa si es GET o si es POST y el login falló simulado)
    context = {
        'message': message,
        'username_attempted': username_attempted,
        # 'is_suspicious' ya no se necesita aquí para mostrar el mensaje principal,
        # pero si quisieras mostrar si _este_ intento particular fue marcado como sospechoso,
        # sería más complejo (ej: buscar el registro recién creado para este usuario/timestamp).
        # Por simplicidad académica, solo mostramos el resultado del login principal.

        # Pasamos el total de intentos sospechosos detectados (obtenido del modelo por la vista)
        'total_suspicious_detected': SuspiciousLoginAttempt.objects.count()
    }

    return render(request, 'security/login.html', context)


# --- Vista para listar todos los intentos sospechosos detectados ---
# Esta vista no necesita cambios ya que solo lee del modelo
def list_suspicious_attempts_view(request):
    attempts = SuspiciousLoginAttempt.objects.all()
    context = {
        'suspicious_attempts': attempts,
        'total_suspicious_detected': attempts.count()
    }
    return render(request, 'security/list_suspicious.html', context)