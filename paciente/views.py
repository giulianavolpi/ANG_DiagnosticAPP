from django.shortcuts import render
from .logic.logic_paciente import get_pacientes
#PARA ERRORES
from diagnosticapp.utils.error_simulation import get_error_stats # Ajusta la ruta de importación

def pacientes_list(request):
    """
    Obtiene el doctor_id de la petición GET y llama a la función de la lógica para obtener
    los pacientes asociados al doctor, llamando a la función de
    'get_pacientes'. Luego, renderiza la plantilla 'paciente/pacientes.html'
    con el contexto de la lista de pacientes.

    Args:
        request (HttpRequest): Objeto de la petición HTTP que contiene los parámetros de la solicitud.

    Returns:
        HttpResponse: Respuesta renderizada con la plantilla 'paciente/pacientes.html' y el contexto con la lista de pacientes.
    """
    doctor_id = request.GET.get('doctor_id')
    pacientes_obtenidos = None # Inicializar la variable para el resultado de la lógica
    error_simulado_en_esta_llamada = False # Flag para indicar error simulado en esta petición

    if doctor_id:
        try:
            doctor_id = int(doctor_id)
            # Llama a la función de lógica con el doctor_id
            # Esta llamada ahora puede retornar None debido al decorador
            pacientes_obtenidos = get_pacientes(doctor_id)

            # --- ¡Nueva Lógica de Detección de Error Simulado! ---
            if pacientes_obtenidos is None:
                # Si la función retornó None, es nuestro error simulado
                error_simulado_en_esta_llamada = True
                # Podrías querer registrar esto aquí si necesitas logging adicional a lo del decorador
                # logger.error(f"Error simulado detectado en vista para doctor_id {doctor_id}")
                # Para mostrar *algo* en la tabla aunque haya error, puedes pasar una lista vacía
                # pacientes_obtenidos = [] # <- Decide si quieres mostrar tabla vacía o dejar None
                                         #    Si dejas None, el template debe manejarlo.
                                         #    En el template modificado abajo, manejo el None.
            # --- Fin Nueva Lógica ---

        except ValueError:
            # Manejar caso donde doctor_id no es un entero si es necesario
            # Por ahora, simplemente no se llama a get_pacientes si falla la conversión
            pass # o podrías setear un error_message en el context

    # Obtén las estadísticas acumuladas de errores
    error_stats = get_error_stats()

    context = {
        # 'pacientes_list': pacientes_obtenidos if pacientes_obtenidos is not None else [], # Opción 1: Siempre pasar lista o lista vacía
        'pacientes_list': pacientes_obtenidos, # Opción 2: Pasar None si hubo error. El template debe manejarlo. Elegimos esta para distinguirlo claramente.
        'error_simulado_en_esta_llamada': error_simulado_en_esta_llamada, # Pasa el flag
        'error_stats': error_stats, # Pasa las estadísticas acumuladas
        'doctor_id_buscado': doctor_id if isinstance(doctor_id, int) else None # Opcional: pasar el ID buscado al template
    }

    return render(request, 'paciente/pacientes.html', context)
