# diagnosticapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Importa reverse para poder redirigir a la URL de login por nombre
from django.urls import reverse # Necesario

# def index(request): # <<< Tu vista original
#    return render(request, 'index.html')

# --- Vista Principal (Modificada para Requerir Sesión Simulada) ---
def index(request):
    # >>> Verificar estado de autenticación simulado en la sesión <<<
    is_simulated_authenticated = request.session.get('simulated_authenticated', False)

    if not is_simulated_authenticated:
        # Si no está "autenticado" simulado, redirige a la página de login
        # Usamos reverse('login') para obtener la URL por su nombre (definido en security/urls.py)
        return redirect(reverse('login'))

    # Si está "autenticado" simulado, renderiza la página principal normalmente
    # Puedes incluso pasar el nombre de usuario simulado si lo guardaste en la sesión
    simulated_username = request.session.get('simulated_username', 'Usuario Desconocido')
    context = {
        'simulated_username': simulated_username,
        # ... otros datos para tu index.html si los necesitas ...
    }
    return render(request, 'index.html', context)

# ... tu vista healthCheck ...
def healthCheck(request):
    return HttpResponse('ok')