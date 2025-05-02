import time
import random

def extract_medical_history(patients):
    """
    Simula la validación de la existencia de los pacientes en el sistema de historias clínicas del hospital
    generando un delay aleatorio entre 15 y 30 ms.

    Args:
        patients (QuerySet): Un QuerySet de pacientes.

    Returns:
        list: Una lista de diccionarios con la información de los pacientes que existen en el sistema de historias
        clínicas del hospital.
    """
    # Simula el delay de 15 a 30 ms
    time.sleep(random.uniform(0.015, 0.03))

    # Por cada paciente, si existe en el sistema del hospital, se guarda su información
    patients_data = []
    for patient in patients:

        paciente_info = {
            'id': patient.id,
            'nombres': patient.nombres,
            'apellidos': patient.apellidos,
            'edad': patient.edad,
            'historia_clinica': f"Historia Clinica del paciente {patient.id}"
        }
        patients_data.append(paciente_info)

    return patients_data
