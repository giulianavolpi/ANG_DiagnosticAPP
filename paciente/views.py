import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from diagnosticapp.utils.error_simulation import get_error_stats

from .models import SimulationStats

# Internal endpoints of your diagnostic app instances
DIAGNOSTIC_HOSTS = [
    "http://10.128.0.53:8000",
    "http://10.128.0.54:8000",
    "http://10.128.0.55:8000",
]

def pacientes_list(request):
    # 1. Parse and normalize doctor_id
    raw_id = request.GET.get("doctor_id")
    try:
        doctor_id = int(raw_id) if raw_id is not None else None
    except ValueError:
        doctor_id = None

    # 2. Fan out GET /pacientes/ to each diagnostic host
    responses = []
    for host in DIAGNOSTIC_HOSTS:
        url = f"{host}/pacientes/?doctor_id={doctor_id}"
        req = Request(url, headers={"Accept": "application/json"})
        try:
            with urlopen(req, timeout=5) as resp:
                data = resp.read().decode("utf-8")
                responses.append(json.loads(data))
        except (HTTPError, URLError) as e:
            responses.append({"error": str(e)})

    # 3. Compare the JSON responses
    serialized = [json.dumps(r, sort_keys=True) for r in responses]
    all_same = len(set(serialized)) == 1
    error_detectado_en_esta_llamada = not all_same

    # 4. Update your SimulationStats counters
    stats, _ = SimulationStats.objects.get_or_create(pk=4)
    SimulationStats.objects.filter(pk=4).update(total_calls=F("total_calls") + 1)
    if error_detectado_en_esta_llamada:
        SimulationStats.objects.filter(pk=4).update(simulated_errors=F("simulated_errors") + 1)

    # 5. Prepare the list of pacientes for the template
    #    If they all agree, use the common result; otherwise you can choose
    #    e.g. to show the first or an empty list. Here we pick the first.
    pacientes_obtenidos = responses[0] if all_same else responses[0]

    # 6. Build and return the context for render()
    context = {
        "pacientes_list": pacientes_obtenidos,
        "error_simulado_en_esta_llamada": error_detectado_en_esta_llamada,
        "doctor_id_buscado": doctor_id if isinstance(doctor_id, int) else None,
    }
    return render(request, "paciente/pacientes.html", context)


from django.http import JsonResponse

def errores(request):
    # 1. Fetch counts
    detected_errors = get_error_stats(4)
    simulated_errors = (
        get_error_stats(1)
        + get_error_stats(2)
        + get_error_stats(3)
    )

    # 2. Compute percentage (avoid division by zero)
    if simulated_errors > 0:
        porcentaje_detectado = (detected_errors / simulated_errors) * 100
    else:
        porcentaje_detectado = 0.0

    # 3. Build response data
    data = {
        "errores_simulados": simulated_errors,
        "errores_detectados": detected_errors,
        "porcentaje_errores_detectados": round(porcentaje_detectado, 2),
    }

    # 4. Return as JSON
    return JsonResponse(data)

