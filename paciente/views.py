from django.http import JsonResponse
from .logic.logic_paciente import get_pacientes

def pacientes_list(request):
    """
    GET /pacientes/?doctor_id=<id>
    Returns: JSON array of pacientes (or empty list on simulated error)
    """
    # 1. Parse doctor_id
    raw_id = request.GET.get("doctor_id")
    try:
        doctor_id = int(raw_id) if raw_id is not None else None
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid doctor_id"}, status=400)

    # 2. Fetch pacientes (None signals simulated error)
    pacientes = get_pacientes(doctor_id) if doctor_id is not None else []
    if pacientes is None:
        pacientes = []  # simulated error → empty list

    # 3. Return as JSON array (safe=False allows top-level list)
    return JsonResponse(pacientes, safe=False)
