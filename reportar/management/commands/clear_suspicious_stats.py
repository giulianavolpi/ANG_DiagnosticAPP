# reportar/management/commands/clear_suspicious_stats.py

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
# from django.contrib.auth import get_user_model # Opcional: si quieres verificar si es superuser

# Importa los modelos de ambas aplicaciones
from heuristica.models import GeneratedSuspiciousAttempt
from reportar.models import DetectedSuspiciousAttempt

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Limpia todos los registros de intentos sospechosos generados por heurística y detectados por reportar (sin confirmación).' # Actualizado el help text

    # Ya no necesitamos el argumento --no-input si no hay confirmación manual
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--no-input',
    #         action='store_true',
    #         help='No pedir confirmación antes de limpiar la base de datos.',
    #     )

    def handle(self, *args, **options):
        # Mensaje de advertencia sigue siendo útil para saber qué hace el comando
        self.stdout.write("⚠️ ADVERTENCIA: Este comando eliminará TODOS los registros de intentos sospechosos sin confirmación.")
        self.stdout.write(f"Tablas a limpiar: {GeneratedSuspiciousAttempt._meta.db_table} y {DetectedSuspiciousAttempt._meta.db_table}")

        # Opcional: Verificar si el usuario que ejecuta el comando es superuser (requiere autenticación de Django)
        # User = get_user_model()
        # try:
        #     # Esto asume que estás ejecutando manage.py con un usuario autenticado,
        #     # lo cual no es el caso típico para comandos de management.
        #     # Una verificación más simple es solo la confirmación manual (que hemos quitado).
        #     pass
        # except User.DoesNotExist:
        #     pass # No hay usuario autenticado.


        # --- BLOQUE DE CONFIRMACIÓN MANUAL ELIMINADO ---
        # if not options['no_input']:
        #     confirm = input("¿Estás ABSOLUTAMENTE seguro de que quieres continuar? Escribe 'yes' para confirmar: ")
        #     if confirm.lower() != 'yes':
        #         raise CommandError("Limpieza cancelada por el usuario.")
        # --- FIN BLOQUE DE CONFIRMACIÓN MANUAL ELIMINADO ---


        self.stdout.write("Iniciando proceso de limpieza (sin confirmación)...") # Actualizado el mensaje

        try:
            # Usar una transacción para asegurar que ambas eliminaciones se completen o ninguna
            with transaction.atomic():
                # Eliminar todos los objetos del modelo GeneratedSuspiciousAttempt
                generated_count, _ = GeneratedSuspiciousAttempt.objects.all().delete()
                self.stdout.write(f"✅ Eliminados {generated_count} registros de {GeneratedSuspiciousAttempt._meta.db_table}.")

                # Eliminar todos los objetos del modelo DetectedSuspiciousAttempt
                detected_count, _ = DetectedSuspiciousAttempt.objects.all().delete()
                self.stdout.write(f"✅ Eliminados {detected_count} registros de {DetectedSuspiciousAttempt._meta.db_table}.")

            self.stdout.write(self.style.SUCCESS("🎉 Limpieza de estadísticas de simulación de errores completada exitosamente."))

        except Exception as e:
            # Si algo falla, la transacción se revertirá automáticamente
            logger.error(f"❌ ERROR FATAL durante la limpieza de estadísticas: {e}", exc_info=True)
            raise CommandError(f"❌ Ocurrió un error durante la limpieza: {e}")

