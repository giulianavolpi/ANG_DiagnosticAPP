import time
import random

def check_doctor_existence(doctor_id):
    """
    Simula la validación de la existencia del médico en el sistema del hospital
    y la validación de que el médico tenga acceso a la información de los pacientes
    con los que está asociado en nuestro sistema, generando un delay aleatorio entre 
    15 y 30 ms.

    Args:
    doctor_id (int): El id del médico

    Returns:
    bool: True si el médico existe y tiene acceso a la información
    de los pacientes (con una probabilidad del 80%), False
    en caso contrario (con una probabilidad del 20%).
    """

    # Simula el delay de 15 a 30 ms
    time.sleep(random.uniform(0.015, 0.03))

    return True #Lo cambio porq ya no necesitamos
