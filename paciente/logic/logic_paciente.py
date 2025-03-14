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
        si el doctor existe y los pacientes existen (en los sistemas del hospital). None si el doctor no existe en el sistema
        del hospital o una lista vacía si los pacientes no existen en el sistema de historias clínicas del hospital o no hay pacientes
        menores de edad asociados al doctor.
    """
    # Revisa si el doctor existe en el sistema del hospital
    if not check_doctor_existence(doctor_id):

        return None

    # Filtra los pacientes distintos que son menores de edad y están asignados al doctor
    patients = Paciente.objects.filter(edad__lt=18, medicos__id=doctor_id).distinct()

    # Mantiene solo los pacientes que efectivamente existen en el sistema de historias clínicas del hospital
    patients_data = extract_medical_history(patients)

    # return pacientes_data
    return patients_data
