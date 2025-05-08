from django.apps import AppConfig

class HeuristicaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heuristica'
    verbose_name = 'Heurística de Seguridad'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación 'heuristica' está lista.
        Importamos el módulo signals para que las definiciones y posibles
        conexiones internas (si las hubiera) se registren.
        """
        # Importar el módulo signals para definir las esñales
        from . import signals 

        # NOTA: La conexión del receptor (que estará en reportar)
        # se hará en el apps.py de la app 'reportar'.
        # Aquí no necesitamos conectar nada a menos que heuristica
        # tuviera receptores propios para otras señales.