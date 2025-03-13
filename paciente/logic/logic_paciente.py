# paciente/logic/logic_paciente.py
from ..models import Paciente
from hospital.logic.logic_hospital import check_doctor_existence
from historiaClinica.logic.logic_historia_clinica import extract_medical_history

def get_pacientes_menores_de_edad(doctor_id):
    """
    Obtener la lista de pacientes menores de edad asignados a un doctor, realizando
    las validaciones necesarias.

    Args:
        doctor_id (int): El id del doctor.

    Returns:
        list: Una lista de diccionarios con la información de los pacientes menores de edad asignados al doctor (en nuestro sistema)
        si el doctor existe y los pacientes existen (en los sistemas del hospital), de lo contrario, retorna None.
    """
    # Revisa si el doctor existe en el sistema del hospital
    if not check_doctor_existence(doctor_id):

        return None

    # Filtra los pacientes distintos que son menores de edad y están asignados al doctor
    pacientes = Paciente.objects.filter(edad__lt=18, medicos__id=doctor_id).distinct()

    # Por cada paciente, si existe en el sistema del hospital, se guarda su información
    pacientes_data = []
    for paciente in pacientes:
        history = extract_medical_history(paciente.id)
        if history:
            paciente_info = {
                'id': paciente.id,
                'nombres': paciente.nombres,
                'apellidos': paciente.apellidos,
                'edad': paciente.edad,
                'historia_clinica': history
            }
            pacientes_data.append(paciente_info)

    return pacientes_data
