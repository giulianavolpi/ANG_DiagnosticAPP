# security/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random  # Necesario para simular el resultado del login principal
import logging
# Importa reverse para poder redirigir usando nombres de URL
from django.urls import reverse

# Importa la señal personalizada que creaste
from .signals import login_attempt # El receptor de esta señal está en signals.py

# Importa el modelo SOLO para obtener el contador total y la lista para la vista de historial
from .models import SuspiciousLoginAttempt # Usado para SuspiciousLoginAttempt.objects.count() y .all()


logger = logging.getLogger(__name__)


# Maneja la visualización del formulario GET y el procesamiento de datos POST.
# Emite la señal de intento de login y simula el resultado del login principal.
def login_view(request):
    message = None
    username_attempted = None
    # is_suspicious_result ya no se usa directamente aquí para el mensaje principal

    if request.method == 'POST':
        # --- 1. Procesar datos del formulario POST ---
        username_attempted = request.POST.get('username')

        if not username_attempted:
            # Si el nombre de usuario está vacío, mostramos un mensaje de error de formulario
            message = "Por favor, ingrese un nombre de usuario."
            logger.warning("VIEW: Intento de login con usuario vacío.")
            # La señal NO se emite si no hay usuario intentado válido para la simulación.
        else:
            # --- 2. Emitir la Señal de Intento de Login (El Evento Ocurrió) ---
            # Esto notifica a cualquier receptor (como nuestro detector de sospecha)
            # que un intento de login con este usuario ha ocurrido.
            # La lógica de simulación de sospecha y guardado en DB ocurre en el receptor.
            login_attempt.send(sender=request, username=username_attempted, request=request)
            logger.info(f"VIEW: Señal 'login_attempt' emitida para usuario: {username_attempted}")
            # --- Fin Emitir Señal ---

            # --- 3. Simular el Resultado del Login Principal ---
            # Esta lógica decide si el login parece "exitoso" o "fallido" desde la perspectiva del usuario
            # que interactúa con la página. Esto es SEPARADO de si fue marcado como sospechoso
            # por el receptor de señal que corre en segundo plano (sincrónicamente).
            if random.random() < 0.8: # Ej: 80% de probabilidad de "login principal exitoso" simulado
                login_successful_simulated = True
                message = f"Login para '{username_attempted}' simulado como exitoso."
                logger.info(f"VIEW: Login principal simulado exitoso para usuario: {username_attempted} -> Marcando sesión y redirigiendo.")

                # >>> 4. Marcar al usuario como "autenticado" en la sesión si el login principal fue exitoso simulado <<<
                request.session['simulated_authenticated'] = True
                request.session['simulated_username'] = username_attempted # Opcional: guardar el nombre de usuario simulado
                # Reinicia el timeout de la sesión para mantenerla activa
                request.session.set_expiry(0) # 0 significa que la sesión expira cuando se cierra el navegador

                # --- 5. Redirigir a la página principal si el login principal fue "exitoso" simulado ---
                # Usamos reverse para obtener la URL por su nombre, por si cambia en el futuro.
                # Asumimos que la URL raíz '/' tiene el nombre 'index' o similar, o simplemente usamos '/' si no tiene nombre.
                # return redirect(reverse('index')) # Si la URL raíz tiene nombre 'index'
                return redirect('/') # Si la URL raíz no tiene nombre o es simplemente '/'

            else:
                # --- 6. Simulación de "login principal fallido" ---
                login_successful_simulated = False
                message = f"Login para '{username_attempted}' simulado como FALLIDO (credenciales inválidas)."
                logger.info(f"VIEW: Login principal simulado fallido para usuario: {username_attempted} -> Mostrando mensaje de error.")
                # --- 7. Asegurarse de que la sesión NO marque como autenticado si el login falló simulado ---
                # Esto es importante para que la vista index lo bloquee.
                request.session['simulated_authenticated'] = False
                if 'simulated_username' in request.session:
                     del request.session['simulated_username']

        # --- Este código se ejecuta para peticiones GET y para peticiones POST que NO redirigieron ---
        # Preparar el contexto para renderizar el template
    context = {
        'message': message, # Mensaje del resultado del POST o None para GET
        'username_attempted': username_attempted, # Nombre de usuario del POST o None para GET
        # 'is_suspicious' ya no se usa aquí para el mensaje principal.

        # --- 8. Pasar el total de intentos sospechosos detectados para mostrar en el template ---
        # Esto SÍ refleja los eventos guardados en la DB por el receptor de señal.
        'total_suspicious_detected': SuspiciousLoginAttempt.objects.count()
    }

    # --- 9. Renderizar el template de login ---
    # Este es el retorno final para peticiones GET y para POST fallidos simulados.
    return render(request, 'security/login.html', context)


# --- Vista para listar todos los intentos sospechosos detectados ---
# Esta vista solo lee del modelo SuspiciousLoginAttempt y muestra la lista.
# No necesita cambios después de la reestructuración de señales.
def list_suspicious_attempts_view(request):
    attempts = SuspiciousLoginAttempt.objects.all()
    context = {
        'suspicious_attempts': attempts,
        'total_suspicious_detected': attempts.count()
    }
    return render(request, 'security/list_suspicious.html', context)