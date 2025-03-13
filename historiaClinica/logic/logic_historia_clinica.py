import time
import random

def extract_medical_history(patient_id):
    """
    Simula la validación de la existencia del paciente en el sistema de historia clínica del hospital
    generando un delay aleatorio entre 15 y 30 ms.

    Args:
        patient_id (int): El id del paciente.

    Returns:
        str: Historia clínica del paciente si existe (con una probabilidad del 80%),
        None en caso contrario (con una probabilidad del 20%).
    """
    time.sleep(random.uniform(0.015, 0.03))

    if random.random() < 0.8:
        return f"Historia Clinica del paciente {patient_id}"
    else:
        return None
