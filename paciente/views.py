from django.shortcuts import render
from .logic.logic_paciente import get_pacientes_menores_de_edad

def pacientes_list(request):
    """
    Obtiene el doctor_id de la petición GET y llama a la función de lógica para obtener
    los pacientes menores de edad asociados a ese doctor llamando a la función de
    la lógica 'get_pacientes_menores_de_edad'. Luego, renderiza la plantilla 'paciente/pacientes.html'
    con el contexto de la lista de pacientes.

    Args:
        request (HttpRequest): Objeto de la petición HTTP que contiene los parámetros de la solicitud.

    Returns:
        HttpResponse: Respuesta renderizada con la plantilla 'paciente/pacientes.html' y el contexto con la lista de pacientes.
    """
    # Extrae el doctor_id de los parámetros GET
    doctor_id = request.GET.get('doctor_id')

    if doctor_id:
        doctor_id = int(doctor_id)

    # Llama a la función de lógica con el doctor_id
    pacientes = get_pacientes_menores_de_edad(doctor_id)

    context = {
        'pacientes_list': pacientes
    }

    return render(request, 'paciente/pacientes.html', context)
