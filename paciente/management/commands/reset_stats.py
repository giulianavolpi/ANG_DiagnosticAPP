# paciente/management/commands/reset_stats.py

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction # Opcional, para mayor seguridad
from diagnosticapp.utils.error_simulation import reset_error_stats # Asegúrate de la ruta correcta

class Command(BaseCommand):
    help = 'Reinicia los contadores de simulación de errores en la base de datos.'

    # def add_arguments(self, parser):
    #     # Puedes añadir argumentos si quisieras, por ejemplo, para confirmar
    #     parser.add_argument(
    #         '--no-input', action='store_true', help='No pedir confirmación.',
    #     )

    def handle(self, *args, **options):
        self.stdout.write("Intentando reiniciar los contadores de simulación de errores...")

        # if not options['no_input']:
        #     confirm = input("¿Estás seguro de que quieres reiniciar los contadores? (yes/no): ")
        #     if confirm.lower() != 'yes':
        #         self.stdout.write("Reinicio cancelado.")
        #         return

        try:
            # Opcional: Usar una transacción para asegurar que todo el reset sea atómico
            # Aunque nuestra función reset_error_stats es simple (una eliminación),
            # en lógicas más complejas una transacción es buena idea.
            # with transaction.atomic():
            reset_error_stats()
            self.stdout.write(self.style.SUCCESS("Contadores de simulación de errores reiniciados en la base de datos."))
        except Exception as e:
            # Manejar cualquier error durante el reset
            raise CommandError(f"Error al reiniciar los contadores: {e}")