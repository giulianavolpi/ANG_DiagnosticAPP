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
        # Importar el receptor que hemos definido
        from reportar.logic import logic_reportar # Esto importa receivers.py

        # Importar la señal de la app 'heuristica' que queremos escuchar
        from heuristica.signals import heuristica_checked # <<< Importamos la señal de OTRA app

        # --- Conectar la señal 'heuristica_checked' al receptor 'report_suspicious_receiver' ---
        # No especificamos un sender aquí porque la señal de heuristica es personalizada
        # y el receptor debe escucharla sin importar quién la emite (aunque solo heuristica la emite).
        heuristica_checked.connect(logic_reportar.report_suspicious_receiver)

        # Puedes añadir más conexiones si reportar tuviera que escuchar otras señales