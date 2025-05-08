# heuristica/signals.py
import django.dispatch

# Define la señal que heuristica emitirá después de su chequeo.
# Pasará el nombre de usuario y si lo marcó como sospechoso.
heuristica_checked = django.dispatch.Signal() # provide_args=['username', 'is_suspicious'] # Opcional pero buena práctica