# pomodoro_app/admin.py

from django.contrib import admin
from .models import PomodoroSession, SessaoEstudo, MetaDiaria

@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tecnica', 'modalidade', 'ciclos_completados', 'tempo_total_estudado', 'em_andamento']
    list_filter = ['tecnica', 'modalidade', 'em_andamento']
    search_fields = ['user__username']

@admin.register(SessaoEstudo)
class SessaoEstudoAdmin(admin.ModelAdmin):
    list_display = ['pomodoro_session', 'status', 'ciclo_numero', 'tempo_inicio', 'distracoes']
    list_filter = ['status']

@admin.register(MetaDiaria)
class MetaDiariaAdmin(admin.ModelAdmin):
    list_display = ['user', 'data', 'meta_minutos', 'minutos_estudados', 'concluida']
    list_filter = ['data', 'concluida']