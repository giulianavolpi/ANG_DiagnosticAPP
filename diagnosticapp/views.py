# diagnosticapp/views.py
from django.shortcuts import render, redirect # redirect ya no es estrictamente necesario en index, pero no molesta
from django.http import HttpResponse
# Ya no necesitas reverse aquí si index no redirige a login
# from django.urls import reverse

# --- Vista Principal Original ---
def index(request):
    # Ya no verificamos la sesión simulada aquí.
    # Simplemente renderizamos la plantilla index.html.
    return render(request, 'index.html')

def healthCheck(request):
    return HttpResponse('ok')