# login/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Importamos la función de heurística
from heuristica.logic.logic_heuristica import check_suspicious # <<< Importación de otra app

# Necesitaremos reverse para redirigir a la URL de login si no se pasa el ID
from django.urls import reverse

# Opcional: logging
import logging
logger = logging.getLogger(__name__)


def login_view(request):
    """
    Maneja el formulario de login GET/POST y el login via GET param 'id'.
    Llama a la heurística para chequear si es sospechoso y decide la respuesta.
    """
    username = None
    message = None
    heuristica_result = None # Almacenará el resultado de la heurística

    # --- 1. Obtener el nombre de usuario ---
    # Priorizamos POST (formulario), luego GET por URL, si no, está vacío
    if request.method == 'POST':
        username = request.POST.get('username')
        logger.info(f"LOGIN VIEW: Petición POST recibida para login con usuario: {username}")
    elif request.method == 'GET':
         # Verificamos si el parámetro 'id' está en los parámetros GET
        username = request.GET.get('id')
        logger.info(f"LOGIN VIEW: Petición GET recibida para login con ID (usuario): {username}")

    # --- 2. Validar si se obtuvo un nombre de usuario ---
    if not username:
        # Si no hay usuario ni en POST ni en GET 'id', mostramos el formulario vacío
        message = "Por favor, ingrese un nombre de usuario."
        logger.warning("LOGIN VIEW: No se proporcionó nombre de usuario en la petición.")
        # No llamamos a la heurística si no hay usuario

        # Renderizamos el formulario vacío
        context = {'message': message}
        return render(request, 'login/login.html', context)

    # --- 3. Si hay nombre de usuario, llamar a la Heurística ---
    # La función check_suspicious vive en la app 'heuristica'
    try:
        # Llamamos a la función de la app heuristica
        # La heuristica guardará sus errores GENERADOS, emitirá una señal,
        # y nos devolverá True si lo marcó como sospechoso, False si no.
        # Puedes pasar una probabilidad diferente si quieres, pero la heuristica
        # también tiene una probabilidad por defecto.
        heuristica_result = check_suspicious(username) # Aquí llamamos a la lógica de heuristica

        logger.info(f"LOGIN VIEW: Llamada a heuristica para usuario '{username}', resultado: {heuristica_result}")

        # --- 4. Decidir la respuesta de login principal basada en el resultado de la Heurística ---
        # Simulación de login principal: Permite acceso (redirigir) si la heurística
        # NO lo marcó como sospechoso. Si SÍ lo marcó, se impide el acceso.
        # Podríamos añadir una simulación ADICIONAL de "credenciales válidas" aquí si quisieras,
        # pero por simplicidad, el acceso principal depende SÓLO de la heurística.

        if not heuristica_result:
            # Si la heuristica NO lo marcó como sospechoso
            message = f"Login para '{username}' simulado como exitoso (No sospechoso)."
            logger.info(f"LOGIN VIEW: Login simulado exitoso y no sospechoso para '{username}' -> Redirigiendo.")
            # >>> Aquí iría la lógica para marcar la sesión como autenticado si fuera necesario persistir <<<
            # request.session['simulated_authenticated'] = True
            # request.session['simulated_username'] = username
            # request.session.set_expiry(0) # Configurar expiración de sesión
            # --- Redirigir a la página principal (simula entrada) ---
            # Usamos reverse para obtener la URL raíz si está nombrada, o simplemente '/'
            # return redirect(reverse('index')) # Si la URL raíz se llama 'index'
            return redirect('/') # Si la URL raíz es simplemente '/'


        else: # heuristica_result is True
            # Si la heuristica SÍ lo marcó como sospechoso
            message = f"Login para '{username}' marcado como SOSPECHOSO por la heurística. Acceso impedido."
            logger.warning(f"LOGIN VIEW: Login para '{username}' marcado como SOSPECHOSO. Impidiendo acceso.")
            # >>> Aquí iría la lógica para asegurar que la sesión NO esté marcada como autenticado <<<
            # request.session['simulated_authenticated'] = False
            # if 'simulated_username' in request.session: del request.session['simulated_username']
            # Nos quedamos en la página de login mostrando el mensaje de sospecha

    except Exception as e:
        # Manejar errores si la llamada a la heurística falla por alguna razón
        message = f"Ocurrió un error al procesar su solicitud de login: {e}"
        logger.error(f"LOGIN VIEW: Error llamando a la heurística para '{username}': {e}", exc_info=True)
        # Nos quedamos en la página de login mostrando el mensaje de error

    # --- Si llegamos aquí, significa que no hubo redirección ---
    # Preparar el contexto y renderizar el template de login
    # Solo mostraremos el mensaje si no hubo redirección.
    context = {
        'message': message, # Mensaje del resultado del POST/GET (si no hubo redirección)
        'username_attempted': username, # Pasamos el usuario intentado al template
        # Otros datos si los necesitas en el template, como el resultado de la heurística
        # 'heuristica_result': heuristica_result, # Puedes pasarlo si quieres mostrarlo en el template
    }

    # --- Renderizar el template de login ---
    # Este es el retorno final para peticiones GET sin 'id' y para POST/GET 'id' donde no hubo redirección (por sospecha o error).
    return render(request, 'login/login.html', context)