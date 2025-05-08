# reportar/apps.py
from django.apps import AppConfig

class ReportarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reportar'
    verbose_name = 'Reportes de Seguridad' # Nombre más amigable

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación 'reportar' está lista.
        Aquí conectamos el receptor a la señal emitida por la app 'heuristica'.
        """
        # Importar la función receptora desde su nueva ubicación
        from .logic.logic_reportar import report_suspicious_receiver # <<< RUTA CORREGIDA

        # Importar la señal de la app 'heuristica' que queremos escuchar
        from heuristica.signals import heuristica_checked # Correcto, no cambia

        # --- Conectar la señal 'heuristica_checked' al receptor 'report_suspicious_receiver' ---
        # No especificamos un sender aquí porque la señal de heuristica es personalizada.
        heuristica_checked.connect(report_suspicious_receiver)