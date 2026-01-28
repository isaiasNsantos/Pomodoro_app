# pomodoro_app/urls.py

# from django.urls import path
# from . import views
# from .views import custom_logout

# app_name = 'pomodoro'

# urlpatterns = [
#     path('', views.pomodoro_dashboard, name='dashboard'),
#     path('iniciar/', views.iniciar_sessao, name='iniciar_sessao'),
#     path('sessao/<int:sessao_id>/atualizar/', views.atualizar_tempo, name='atualizar_tempo'),
#     path('sessao/<int:sessao_id>/proxima/', views.proxima_fase, name='proxima_fase'),
#     path('sessao/<int:sessao_id>/pausar/', views.pausar_sessao, name='pausar_sessao'),
#     path('sessao/<int:sessao_id>/retomar/', views.retomar_sessao, name='retomar_sessao'),
#     path('sessao/<int:sessao_id>/finalizar/', views.finalizar_sessao, name='finalizar_sessao'),
#     path('estatisticas/', views.estatisticas, name='estatisticas'),
#     path('atualizar-meta/', views.atualizar_meta, name='atualizar_meta'),
#     path('logout/', views.custom_logout, name='logout'),
#     path('musicas/', views.musicas_estudo, name='musicas'),
#     path('musicas/upload/', views.upload_musica, name='upload_musica'),
#     path('musicas/criar-playlist/', views.criar_playlist, name='criar_playlist'),
#     path('musicas/<int:musica_id>/deletar/', views.deletar_musica, name='deletar_musica'),
#     path('musicas/<int:musica_id>/play/', views.play_musica, name='play_musica'),
#     path('playlists/<int:playlist_id>/deletar/', views.deletar_playlist, name='deletar_playlist'),
#     path('playlists/<int:playlist_id>/musicas/', views.get_playlist_musicas, name='get_playlist_musicas'),
# ]

# pomodoro_app/urls.py

from django.urls import path
from . import views

app_name = 'pomodoro'

urlpatterns = [
    # URLs principais do Pomodoro
    path('', views.pomodoro_dashboard, name='dashboard'),
    path('iniciar/', views.iniciar_sessao, name='iniciar_sessao'),
    path('sessao/<int:sessao_id>/atualizar/', views.atualizar_tempo, name='atualizar_tempo'),
    path('sessao/<int:sessao_id>/proxima/', views.proxima_fase, name='proxima_fase'),
    path('sessao/<int:sessao_id>/pausar/', views.pausar_sessao, name='pausar_sessao'),
    path('sessao/<int:sessao_id>/retomar/', views.retomar_sessao, name='retomar_sessao'),
    path('sessao/<int:sessao_id>/finalizar/', views.finalizar_sessao, name='finalizar_sessao'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('atualizar-meta/', views.atualizar_meta, name='atualizar_meta'),
    path('logout/', views.custom_logout, name='logout'),
    
    # URLs para músicas
    path('musicas/', views.musicas_estudo, name='musicas'),
    path('musicas/upload/', views.upload_musica, name='upload_musica'),
    path('musicas/criar-playlist/', views.criar_playlist, name='criar_playlist'),
    path('musicas/<int:musica_id>/deletar/', views.deletar_musica, name='deletar_musica'),
    path('musicas/<int:musica_id>/play/', views.play_musica, name='play_musica'),
    path('playlists/<int:playlist_id>/deletar/', views.deletar_playlist, name='deletar_playlist'),
    path('playlists/<int:playlist_id>/musicas/', views.get_playlist_musicas, name='get_playlist_musicas'),
    path('playlists/<int:playlist_id>/usar/', views.usar_playlist, name='usar_playlist'),
]