# security/apps.py
from django.apps import AppConfig

class SecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'security'
    verbose_name = 'Seguridad'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación 'security' está lista.
        Aquí conectamos nuestras señales a sus receptores.
        """
        # Importar las señales y los receptores para poder conectarlos.
        # Esta importación asegura que el código en signals.py (definiciones)
        # se ejecuta antes de intentar conectar.
        from . import signals # <<< Importación necesaria

        # Conectar la señal login_attempt al receptor check_suspicious_login_receiver.
        # El sender es opcional; si no se especifica, el receptor recibirá señales
        # de cualquier emisor de 'login_attempt'. Si especificamos un sender (ej: un modelo),
        # solo recibiría señales de ese modelo. Para nuestra señal personalizada,
        # conectamos sin un sender específico a menos que queramos filtrar por el emisor.
        signals.login_attempt.connect(signals.check_suspicious_login_receiver)

