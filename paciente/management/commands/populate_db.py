# paciente/management/commands/populate_db.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from infoAdmin.models import Medico
from paciente.models import Paciente

class Command(BaseCommand):
    help = (
        "Popula la base de datos con:\n"
        " 1) 250 doctores y 250 pacientes iniciales (con 2–5 doctores cada uno)\n"
        " 2) 100 pacientes adicionales, cada uno asociado a la mitad de los doctores existentes, i.e. "
        "250 doctores y 350 pacientes en total.\n"
    )

    def handle(self, *args, **options):
        fake = Faker()

        # 1. Crear 250 doctores
        self.stdout.write("Creando 250 doctores...")
        doctores = [
            Medico(nombres=fake.first_name(), apellidos=fake.last_name())
            for _ in range(250)
        ]
        Medico.objects.bulk_create(doctores)  # Inserción masiva :contentReference[oaicite:0]{index=0}
        doctores = list(Medico.objects.all())
        self.stdout.write(self.style.SUCCESS(f"{len(doctores)} doctores creados."))

        # 2. Crear 250 pacientes iniciales
        self.stdout.write("Creando 250 pacientes iniciales...")
        pacientes = []
        for _ in range(250):
            p = Paciente(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                edad=random.randint(0, 100)
            )
            p.save()
            pacientes.append(p)
        self.stdout.write(self.style.SUCCESS(f"{len(pacientes)} pacientes iniciales creados."))

        # Asignación inicial: 2–5 doctores aleatorios por paciente
        self.stdout.write("Asignando 2–5 doctores a cada paciente inicial...")
        for p in pacientes:
            num = random.randint(2, 5)
            seleccionados = random.sample(doctores, num)
            p.medicos.set(seleccionados)

        # 3. Crear 100 pacientes adicionales
        self.stdout.write("Creando 100 pacientes adicionales...")
        mitad = len(doctores) // 2
        for _ in range(100):
            p = Paciente(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                edad=random.randint(0, 100)
            )
            p.save()
            asignados = random.sample(doctores, mitad)
            p.medicos.set(asignados)
        self.stdout.write(self.style.SUCCESS(
            f"100 pacientes adicionales creados y asignados a {mitad} doctores cada uno."
        ))

        self.stdout.write(self.style.SUCCESS("Población de la base de datos completada."))
