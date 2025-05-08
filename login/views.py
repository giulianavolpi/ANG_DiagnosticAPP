# login/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Importamos la función de heurística desde su nueva ruta
from heuristica.logic.logic_heuristica import check_suspicious # <<< RUTA CORREGIDA

# Necesitaremos reverse para redirigir a la URL de login si no se pasa el ID
from django.urls import reverse

# Opcional: logging
import logging
logger = logging.getLogger(__name__)


# login/views.py
# ... imports ...

def login_view(request):
    # Inicializaciones (indentación base)
    username = None
    message = None
    heuristica_result = None

    # --- Bloque principal GET/POST ---
    if request.method == 'POST':
        # Lógica para POST (indentación 1)
        username = request.POST.get('username')
        logger.info(f"LOGIN VIEW: Petición POST recibida para login con usuario: {username}")

        # --- Bloque 'Si no hay usuario' DENTRO de POST ---
        if not username:
            # Lógica si NO hay usuario en POST (indentación 2)
            message = "Por favor, ingrese un nombre de usuario."
            logger.warning("LOGIN VIEW: No se proporcionó nombre de usuario en la petición.")
            # No llamamos a la heurística si no hay usuario

            # Preparar contexto DENTRO de este bloque
            context = {'message': message} # (indentación 2)

            # Retornar DENTRO de este bloque
            return render(request, 'login/login.html', context) # <<< ESTA LÍNEA DEBE ESTAR AQUÍ CON ESTA INDENTACIÓN

        # --- Si llegamos aquí, significa que SI había usuario en POST (indentación 1) ---
        # La ejecución continúa aquí SÓLO si username NO estaba vacío en POST.

        # Ahora entramos en el try/except para llamar a la heurística (indentación 1)
        try:
            # Llamada a heurística y lógica de redirección (indentación 2, 3, etc. dentro del try)
            heuristica_result = check_suspicious(username)
            logger.info(f"LOGIN VIEW: Llamada a heuristica para usuario '{username}', resultado: {heuristica_result}")

            if not heuristica_result: # Si NO fue sospechoso (indentación 3)
                 message = f"Login para '{username}' simulado como exitoso (No sospechoso)."
                 logger.info("... Redirigiendo.")
                 return redirect('/') # <<< ESTA LÍNEA DE REDIRECCIÓN ESTÁ AQUÍ (indentación 3)

            else: # Si SÍ fue sospechoso (indentación 3)
                 message = f"Login para '{username}' marcado como SOSPECHOSO..."
                 logger.warning("... Impidiendo acceso.")
                 # No hay return aquí, la ejecución CONTINÚA DESPUÉS de este IF/ELSE interno

        except Exception as e: # Manejo de error de heurística (indentación 2)
             message = f"Ocurrió un error...: {e}"
             logger.error("... Error llamando a la heurística...")
             # No hay return aquí, la ejecución CONTINÚA DESPUÉS del try/except

        # --- Si llegamos aquí, significa que fue POST, había usuario, NO HUBO REDIRECCIÓN (por sospecha o error) ---
        # La ejecución cae aquí para los casos de POST donde nos quedamos en la página.
        # DEBERÍA LLEGAR AQUÍ después del IF/ELSE dentro del try, o después del except.

    # --- Bloque para GET (indentación 1) ---
    elif request.method == 'GET':
        # Lógica para GET (indentación 2)
        username = request.GET.get('id')
        logger.info(f"LOGIN VIEW: Petición GET recibida para login con ID (usuario): {username}")

        if not username: # Si es GET sin 'id' (indentación 3)
            message = "Por favor, ingrese un nombre de usuario."
            logger.warning("LOGIN VIEW: No se proporcionó nombre de usuario en la petición GET sin ID.")
            # No llama a heurística. La ejecución CONTINÚA después de este IF.
            pass # Opcional pass, no necesario

        else: # Si es GET CON 'id' (indentación 3)
            # Si hay usuario en GET, AHORA llamamos a la heurística y procesamos el resultado
            # La lógica es la MISMA que la de POST CON usuario.
            # Podríamos refactorizar esto en una función auxiliar, pero por ahora la repetimos.
            try:
                heuristica_result = check_suspicious(username)
                logger.info(f"LOGIN VIEW: Llamada a heuristica (GET) para '{username}', resultado: {heuristica_result}")

                if not heuristica_result: # Si NO fue sospechoso (indentación 4)
                    message = f"Login para '{username}' simulado como exitoso (No sospechoso - GET)."
                    logger.info("... Redirigiendo (GET).")
                    return redirect('/') # <<< REDIRECCIÓN PARA GET CON ID NO SOSPECHOSO

                else: # Si SÍ fue sospechoso (indentación 4)
                     message = f"Login para '{username}' marcado como SOSPECHOSO (GET). Acceso impedido."
                     logger.warning("... Impidiendo acceso (GET).")
                     # No hay return aquí, la ejecución CONTINÚA DESPUÉS de este IF/ELSE interno

            except Exception as e: # Manejo de error de heurística (indentación 3)
                 message = f"Ocurrió un error... (GET): {e}"
                 logger.error("... Error llamando a la heurística (GET)...")
                 # No hay return aquí, la ejecución CONTINÚA DESPUÉS del try/except

        # --- Si llegamos aquí, significa que fue GET sin 'id', o GET con 'id' donde NO HUBO REDIRECCIÓN (por sospecha o error) ---
        # La ejecución cae aquí para los casos de GET donde nos quedamos en la página.
        # DEBERÍA LLEGAR AQUÍ después de los IF/ELSE/try/except internos de GET.


    # --- Bloque FINAL de renderizado ---
    # ESTE BLOQUE SE EJECUTA para GET (sin 'id' o con 'id' donde no hubo redirect)
    # Y para POST (sin 'username', o con 'username' donde no hubo redirect).
    # Su INDENTACIÓN debe estar al mismo nivel que los bloques 'if request.method == "POST":'
    # y 'elif request.method == "GET":'.

    context = { # <--- Preparación FINAL del contexto
        'message': message, # Mensaje establecido en algún punto anterior o None
        'username_attempted': username, # Usuario establecido en algún punto anterior o None
        # ... otros datos ...
    }

    # Retorno FINAL que SIEMPRE debe ocurrir si no se ejecutó un 'return redirect'
    return render(request, 'login/login.html', context) # <<< ESTA LÍNEA DEBE ESTAR AQUÍ AL NIVEL CORRECTO.