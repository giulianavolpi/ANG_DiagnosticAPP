# heuristica/admin.py
from django.contrib import admin
from .models import GeneratedSuspiciousAttempt

@admin.register(GeneratedSuspiciousAttempt)
class GeneratedSuspiciousAttemptAdmin(admin.ModelAdmin):
     list_display = ('username_attempted', 'timestamp')
     list_filter = ('timestamp',)
     search_fields = ('username_attempted',)
     readonly_fields = ('timestamp',)