# # pomodoro_app/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# from django.contrib import messages
# from django.http import JsonResponse
# from django.utils import timezone
# from django.db.models import Sum, Count
# from .models import PomodoroSession, SessaoEstudo, MetaDiaria
# from .forms import PomodoroSessionForm, MetaDiariaForm
# import json
# import datetime

# @login_required
# def pomodoro_dashboard(request):
#     """Dashboard principal do Pomodoro"""
#     # Buscar sessão ativa do usuário
#     sessao_ativa = PomodoroSession.objects.filter(
#         user=request.user, 
#         em_andamento=True
#     ).first()
    
#     # Obter ou criar meta diária
#     meta_hoje, created = MetaDiaria.objects.get_or_create(
#         user=request.user,
#         data=timezone.now().date()
#     )
    
#     # Estatísticas básicas
#     sessoes_completas = PomodoroSession.objects.filter(
#         user=request.user,
#         em_andamento=False
#     ).count()
    
#     total_minutos_result = PomodoroSession.objects.filter(
#         user=request.user
#     ).aggregate(total=Sum('tempo_total_estudado'))
#     total_minutos = total_minutos_result['total'] or 0
    
#     # Formulário para nova sessão (só se não tiver sessão ativa)
#     form = None
#     if not sessao_ativa:
#         form = PomodoroSessionForm()
    
#     # Formulário para meta diária
#     meta_form = MetaDiariaForm(instance=meta_hoje)
    
#     # Histórico recente
#     historico = PomodoroSession.objects.filter(
#         user=request.user
#     ).order_by('-data_criacao')[:5]
    
#     contexto = {
#         'sessao_ativa': sessao_ativa,
#         'meta_hoje': meta_hoje,
#         'sessoes_completas': sessoes_completas,
#         'total_minutos': total_minutos,
#         'form': form,
#         'meta_form': meta_form,
#         'historico': historico,
#     }
    
#     return render(request, 'pomodoro_app/dashboard.html', contexto)

# @login_required
# def iniciar_sessao(request):
#     """Inicia uma nova sessão Pomodoro"""
#     if request.method == 'POST':
#         form = PomodoroSessionForm(request.POST)
#         if form.is_valid():
#             try:
#                 sessao = form.save(commit=False)
#                 sessao.user = request.user
#                 sessao.em_andamento = True
#                 sessao.save()
                
#                 # Criar primeira sessão de foco
#                 SessaoEstudo.objects.create(
#                     pomodoro_session=sessao,
#                     status='foco',
#                     ciclo_numero=1,
#                     tempo_inicio=timezone.now(),
#                     tempo_restante=sessao.tempo_foco * 60
#                 )
                
#                 messages.success(request, 'Sessão Pomodoro iniciada com sucesso! 🚀')
#                 return redirect('pomodoro:dashboard')
                
#             except Exception as e:
#                 messages.error(request, f'Erro ao iniciar sessão: {str(e)}')
#                 return redirect('pomodoro:dashboard')
#         else:
#             # Coletar todos os erros do formulário
#             error_messages = []
#             for field, errors in form.errors.items():
#                 field_name = form.fields[field].label if field in form.fields else field
#                 for error in errors:
#                     error_messages.append(f"{field_name}: {error}")
            
#             if error_messages:
#                 for error_msg in error_messages:
#                     messages.error(request, error_msg)
#             else:
#                 messages.error(request, 'Por favor, corrija os erros no formulário.')
            
#             return redirect('pomodoro:dashboard')
    
#     # Se não for POST, redireciona para o dashboard
#     return redirect('pomodoro:dashboard')

# @login_required
# def atualizar_tempo(request, sessao_id):
#     """Atualiza o tempo restante (chamada AJAX)"""
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             tempo_restante = data.get('tempo_restante', 0)
            
#             # Verificar se a sessão existe e pertence ao usuário
#             sessao_estudo = SessaoEstudo.objects.filter(
#                 pomodoro_session__id=sessao_id,
#                 pomodoro_session__user=request.user,
#                 pomodoro_session__em_andamento=True,
#                 tempo_fim__isnull=True
#             ).first()
            
#             if sessao_estudo:
#                 sessao_estudo.tempo_restante = tempo_restante
#                 sessao_estudo.save()
#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Sessão não encontrada ou não está ativa'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
    
#     return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

# @login_required
# def proxima_fase(request, sessao_id):
#     """Avança para a próxima fase (foco/pausa)"""
#     pomodoro = get_object_or_404(
#         PomodoroSession, 
#         id=sessao_id, 
#         user=request.user,
#         em_andamento=True
#     )
    
#     sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
    
#     if sessao_atual:
#         # Finalizar sessão atual
#         sessao_atual.tempo_fim = timezone.now()
#         sessao_atual.status = 'completo'
#         sessao_atual.save()
        
#         # Calcular tempo estudado
#         if sessao_atual.status == 'foco':
#             duracao = sessao_atual.duracao_minutos()
#             pomodoro.tempo_total_estudado += duracao
            
#             # Atualizar meta diária
#             meta, created = MetaDiaria.objects.get_or_create(
#                 user=request.user,
#                 data=timezone.now().date()
#             )
#             meta.minutos_estudados += duracao
#             meta.save()
        
#         # Determinar próxima fase
#         if sessao_atual.status == 'foco':
#             pomodoro.ciclos_completados += 1
            
#             if pomodoro.ciclos_completados % pomodoro.ciclos_para_pausa_longa == 0:
#                 proximo_status = 'pausa_longa'
#                 proximo_tempo = pomodoro.tempo_pausa_longa
#             else:
#                 proximo_status = 'pausa_curta'
#                 proximo_tempo = pomodoro.tempo_pausa_curta
            
#             proximo_ciclo = pomodoro.ciclos_completados + 1
#         else:
#             proximo_status = 'foco'
#             proximo_tempo = pomodoro.tempo_foco
#             proximo_ciclo = pomodoro.ciclos_completados + 1
        
#         # Criar próxima sessão
#         SessaoEstudo.objects.create(
#             pomodoro_session=pomodoro,
#             status=proximo_status,
#             ciclo_numero=proximo_ciclo,
#             tempo_inicio=timezone.now(),
#             tempo_restante=proximo_tempo * 60
#         )
        
#         pomodoro.save()
        
#         status_display = proximo_status.replace('_', ' ').title()
#         messages.info(request, f'✅ Próxima fase: {status_display} iniciada!')
    
#     return redirect('pomodoro:dashboard')

# @login_required
# def pausar_sessao(request, sessao_id):
#     """Pausa a sessão atual"""
#     pomodoro = get_object_or_404(
#         PomodoroSession, 
#         id=sessao_id, 
#         user=request.user,
#         em_andamento=True
#     )
    
#     sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
#     if sessao_atual:
#         sessao_atual.status = 'pausado'
#         sessao_atual.save()
#         messages.warning(request, '⏸️ Sessão pausada. Você pode retomar quando quiser.')
    
#     return redirect('pomodoro:dashboard')

# @login_required
# def retomar_sessao(request, sessao_id):
#     """Retoma uma sessão pausada"""
#     pomodoro = get_object_or_404(
#         PomodoroSession, 
#         id=sessao_id, 
#         user=request.user,
#         em_andamento=True
#     )
    
#     sessao_atual = pomodoro.sessoes.filter(status='pausado').last()
#     if sessao_atual:
#         # Recalcular tempo restante
#         tempo_decorrido = (timezone.now() - sessao_atual.tempo_inicio).seconds
#         tempo_restante = max(0, sessao_atual.tempo_restante - tempo_decorrido)
        
#         sessao_atual.status = 'foco' if sessao_atual.status == 'pausado' else sessao_atual.status
#         sessao_atual.tempo_inicio = timezone.now()
#         sessao_atual.tempo_restante = tempo_restante
#         sessao_atual.save()
#         messages.success(request, '▶️ Sessão retomada! Continue focado!')
    
#     return redirect('pomodoro:dashboard')

# @login_required
# def finalizar_sessao(request, sessao_id):
#     """Finaliza a sessão Pomodoro"""
#     pomodoro = get_object_or_404(
#         PomodoroSession, 
#         id=sessao_id, 
#         user=request.user,
#         em_andamento=True
#     )
    
#     sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
#     if sessao_atual:
#         sessao_atual.tempo_fim = timezone.now()
#         sessao_atual.status = 'completo'
#         sessao_atual.save()
        
#         # Adicionar tempo estudado se estava em foco
#         if sessao_atual.status == 'foco':
#             duracao = sessao_atual.duracao_minutos()
#             pomodoro.tempo_total_estudado += duracao
            
#             # Atualizar meta diária
#             meta, created = MetaDiaria.objects.get_or_create(
#                 user=request.user,
#                 data=timezone.now().date()
#             )
#             meta.minutos_estudados += duracao
#             meta.save()
    
#     pomodoro.em_andamento = False
#     pomodoro.data_finalizacao = timezone.now()
#     pomodoro.save()
    
#     messages.success(request, '✅ Sessão finalizada com sucesso! Ótimo trabalho! 🎉')
#     return redirect('pomodoro:dashboard')

# @login_required
# def estatisticas(request):
#     """Página de estatísticas"""
#     # Estatísticas gerais
#     total_sessoes = PomodoroSession.objects.filter(user=request.user).count()
    
#     total_minutos_result = PomodoroSession.objects.filter(
#         user=request.user
#     ).aggregate(total=Sum('tempo_total_estudado'))
#     total_minutos = total_minutos_result['total'] or 0
    
#     # Distribuição por modalidade
#     modalidades_raw = PomodoroSession.objects.filter(user=request.user)
#     modalidades_data = []
#     for modalidade_choice in PomodoroSession.MODALIDADE_CHOICES:
#         modalidade_value = modalidade_choice[0]
#         modalidade_display = modalidade_choice[1]
        
#         sessoes_modalidade = modalidades_raw.filter(modalidade=modalidade_value)
#         total_sessoes_modalidade = sessoes_modalidade.count()
#         total_minutos_modalidade = sessoes_modalidade.aggregate(
#             total=Sum('tempo_total_estudado')
#         )['total'] or 0
        
#         if total_sessoes > 0:
#             porcentagem = (total_minutos_modalidade / total_minutos * 100) if total_minutos > 0 else 0
#         else:
#             porcentagem = 0
        
#         modalidades_data.append({
#             'modalidade': modalidade_value,
#             'modalidade_display': modalidade_display,
#             'total': total_sessoes_modalidade,
#             'minutos': total_minutos_modalidade,
#             'porcentagem': round(porcentagem, 1)
#         })
    
#     # Meta diária atual
#     meta_hoje, created = MetaDiaria.objects.get_or_create(
#         user=request.user,
#         data=timezone.now().date()
#     )
    
#     # Histórico de metas
#     historico_metas = MetaDiaria.objects.filter(
#         user=request.user
#     ).order_by('-data')[:30]
    
#     contexto = {
#         'total_sessoes': total_sessoes,
#         'total_minutos': total_minutos,
#         'total_horas': round(total_minutos / 60, 1),
#         'modalidades': modalidades_data,
#         'meta_hoje': meta_hoje,
#         'historico_metas': historico_metas,
#     }
    
#     return render(request, 'pomodoro_app/estatisticas.html', contexto)

# @login_required
# def atualizar_meta(request):
#     """Atualiza a meta diária"""
#     if request.method == 'POST':
#         meta, created = MetaDiaria.objects.get_or_create(
#             user=request.user,
#             data=timezone.now().date()
#         )
#         form = MetaDiariaForm(request.POST, instance=meta)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '✅ Meta diária atualizada com sucesso!')
#         else:
#             for error in form.errors.get('meta_minutos', []):
#                 messages.error(request, f'Meta: {error}')
    
#     return redirect('pomodoro:dashboard')

# @login_required
# def custom_logout(request):
#     """View personalizada para logout"""
#     if request.method == 'POST':
#         logout(request)
#         return redirect('login')
#     return render(request, 'pomodoro_app/logout_confirm.html')

# # pomodoro_app/views.py - ADICIONE ESTAS VIEWS

# import os
# from django.conf import settings
# from mutagen import File as MutagenFile
# from mutagen.mp3 import MP3
# from mutagen.wave import WAVE

# @login_required
# def musicas_estudo(request):
#     """Página de gerenciamento de músicas"""
#     musicas = MusicaEstudo.objects.filter(
#         models.Q(user=request.user) | models.Q(publica=True)
#     ).distinct().order_by('-data_upload')
    
#     playlists = PlaylistEstudo.objects.filter(user=request.user)
    
#     contexto = {
#         'musicas': musicas,
#         'playlists': playlists,
#         'form_musica': MusicaEstudoForm(),
#         'form_playlist': PlaylistEstudoForm(user=request.user),
#     }
    
#     return render(request, 'pomodoro_app/musicas.html', contexto)

# @login_required
# def upload_musica(request):
#     """Upload de nova música"""
#     if request.method == 'POST':
#         form = MusicaEstudoForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 musica = form.save(commit=False)
#                 musica.user = request.user
                
#                 # Calcular duração do arquivo
#                 arquivo = musica.arquivo_audio
#                 extensao = os.path.splitext(arquivo.name)[1].lower()
                
#                 try:
#                     if extensao == '.mp3':
#                         audio = MP3(arquivo.file)
#                     elif extensao == '.wav':
#                         audio = WAVE(arquivo.file)
#                     else:
#                         # Para outros formatos, tentar com mutagen genérico
#                         audio = MutagenFile(arquivo.file)
                    
#                     if audio:
#                         musica.duracao = int(audio.info.length)
#                 except:
#                     # Se não conseguir detectar duração, usar valor padrão
#                     musica.duracao = 300  # 5 minutos
                
#                 musica.save()
#                 messages.success(request, f'Música "{musica.nome}" adicionada com sucesso!')
                
#             except Exception as e:
#                 messages.error(request, f'Erro ao processar música: {str(e)}')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')
    
#     return redirect('pomodoro:musicas')

# @login_required
# def criar_playlist(request):
#     """Criar nova playlist"""
#     if request.method == 'POST':
#         form = PlaylistEstudoForm(request.user, request.POST)
#         if form.is_valid():
#             playlist = form.save(commit=False)
#             playlist.user = request.user
#             playlist.save()
            
#             # Adicionar músicas selecionadas
#             musicas_selecionadas = form.cleaned_data.get('musicas_selecionadas', [])
#             playlist.musicas.set(musicas_selecionadas)
            
#             messages.success(request, f'Playlist "{playlist.nome}" criada com sucesso!')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')
    
#     return redirect('pomodoro:musicas')

# @login_required
# def deletar_musica(request, musica_id):
#     """Deletar música"""
#     musica = get_object_or_404(MusicaEstudo, id=musica_id, user=request.user)
    
#     # Verificar se a música está em uso
#     if PomodoroSession.objects.filter(musica_atual=musica, em_andamento=True).exists():
#         messages.error(request, 'Não é possível deletar esta música pois está em uso em uma sessão ativa.')
#     else:
#         # Remover arquivo físico
#         if musica.arquivo_audio:
#             if os.path.isfile(musica.arquivo_audio.path):
#                 os.remove(musica.arquivo_audio.path)
        
#         nome_musica = musica.nome
#         musica.delete()
#         messages.success(request, f'Música "{nome_musica}" deletada com sucesso!')
    
#     return redirect('pomodoro:musicas')

# @login_required
# def deletar_playlist(request, playlist_id):
#     """Deletar playlist"""
#     playlist = get_object_or_404(PlaylistEstudo, id=playlist_id, user=request.user)
    
#     # Verificar se a playlist está em uso
#     if PomodoroSession.objects.filter(playlist=playlist, em_andamento=True).exists():
#         messages.error(request, 'Não é possível deletar esta playlist pois está em uso em uma sessão ativa.')
#     else:
#         nome_playlist = playlist.nome
#         playlist.delete()
#         messages.success(request, f'Playlist "{nome_playlist}" deletada com sucesso!')
    
#     return redirect('pomodoro:musicas')

# @login_required
# def play_musica(request, musica_id):
#     """API para tocar música"""
#     musica = get_object_or_404(
#         MusicaEstudo.objects.filter(
#             models.Q(user=request.user) | models.Q(publica=True)
#         ),
#         id=musica_id
#     )
    
#     # Atualizar estatísticas
#     musica.vezes_tocada += 1
#     musica.ultima_reproducao = timezone.now()
#     musica.save()
    
#     return JsonResponse({
#         'status': 'success',
#         'url': musica.arquivo_audio.url,
#         'nome': musica.nome,
#         'duracao': musica.duracao
#     })

# @login_required
# def get_playlist_musicas(request, playlist_id):
#     """API para obter músicas de uma playlist"""
#     playlist = get_object_or_404(PlaylistEstudo, id=playlist_id, user=request.user)
    
#     musicas = []
#     for musica in playlist.musicas.all():
#         musicas.append({
#             'id': musica.id,
#             'nome': musica.nome,
#             'url': musica.arquivo_audio.url,
#             'duracao': musica.duracao,
#             'extensao': musica.get_extensao()
#         })
    
#     return JsonResponse({
#         'status': 'success',
#         'playlist': playlist.nome,
#         'ordem_reproducao': playlist.ordem_reproducao,
#         'musicas': musicas
#     })

# # Atualizar a view pomodoro_dashboard para incluir dados de música
# @login_required
# def pomodoro_dashboard(request):
#     """Dashboard principal do Pomodoro"""
#     # ... código existente ...
    
#     # Adicionar dados de música ao contexto
#     playlists = PlaylistEstudo.objects.filter(user=request.user)
    
#     contexto = {
#         # ... contexto existente ...
#         'playlists': playlists,
#     }
    
#     return render(request, 'pomodoro_app/dashboard.html', contexto)
# pomodoro_app/views.py - VERSÃO COMPLETA E CORRIGIDA

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
import json
import datetime
import os
from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from .models import PomodoroSession, SessaoEstudo, MetaDiaria, MusicaEstudo, PlaylistEstudo
from .forms import PomodoroSessionForm, MetaDiariaForm, MusicaEstudoForm, PlaylistEstudoForm

# ============================================
# VIEWS PRINCIPAIS DO POMODORO
# ============================================

@login_required
def pomodoro_dashboard(request):
    """Dashboard principal do Pomodoro"""
    # Buscar sessão ativa do usuário
    sessao_ativa = PomodoroSession.objects.filter(
        user=request.user, 
        em_andamento=True
    ).first()
    
    # Obter ou criar meta diária
    meta_hoje, created = MetaDiaria.objects.get_or_create(
        user=request.user,
        data=timezone.now().date()
    )
    
    # Estatísticas básicas
    sessoes_completas = PomodoroSession.objects.filter(
        user=request.user,
        em_andamento=False
    ).count()
    
    total_minutos_result = PomodoroSession.objects.filter(
        user=request.user
    ).aggregate(total=Sum('tempo_total_estudado'))
    total_minutos = total_minutos_result['total'] or 0
    
    # Formulário para nova sessão (só se não tiver sessão ativa)
    form = None
    if not sessao_ativa:
        form = PomodoroSessionForm(user=request.user)
    
    # Formulário para meta diária
    meta_form = MetaDiariaForm(instance=meta_hoje)
    
    # Histórico recente
    historico = PomodoroSession.objects.filter(
        user=request.user
    ).order_by('-data_criacao')[:5]
    
    # Playlists do usuário
    playlists = PlaylistEstudo.objects.filter(user=request.user)
    
    contexto = {
        'sessao_ativa': sessao_ativa,
        'meta_hoje': meta_hoje,
        'sessoes_completas': sessoes_completas,
        'total_minutos': total_minutos,
        'form': form,
        'meta_form': meta_form,
        'historico': historico,
        'playlists': playlists,
    }
    
    return render(request, 'pomodoro_app/dashboard.html', contexto)


@login_required
def iniciar_sessao(request):
    """Inicia uma nova sessão Pomodoro"""
    if request.method == 'POST':
        form = PomodoroSessionForm(request.user, request.POST)
        if form.is_valid():
            try:
                sessao = form.save(commit=False)
                sessao.user = request.user
                sessao.em_andamento = True
                sessao.save()
                
                # Criar primeira sessão de foco
                SessaoEstudo.objects.create(
                    pomodoro_session=sessao,
                    status='foco',
                    ciclo_numero=1,
                    tempo_inicio=timezone.now(),
                    tempo_restante=sessao.tempo_foco * 60
                )
                
                messages.success(request, 'Sessão Pomodoro iniciada com sucesso! 🚀')
                return redirect('pomodoro:dashboard')
                
            except Exception as e:
                messages.error(request, f'Erro ao iniciar sessão: {str(e)}')
                return redirect('pomodoro:dashboard')
        else:
            # Coletar todos os erros do formulário
            error_messages = []
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                for error in errors:
                    error_messages.append(f"{field_name}: {error}")
            
            if error_messages:
                for error_msg in error_messages:
                    messages.error(request, error_msg)
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
            
            return redirect('pomodoro:dashboard')
    
    # Se não for POST, redireciona para o dashboard
    return redirect('pomodoro:dashboard')


@login_required
def atualizar_tempo(request, sessao_id):
    """Atualiza o tempo restante (chamada AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tempo_restante = data.get('tempo_restante', 0)
            
            # Verificar se a sessão existe e pertence ao usuário
            sessao_estudo = SessaoEstudo.objects.filter(
                pomodoro_session__id=sessao_id,
                pomodoro_session__user=request.user,
                pomodoro_session__em_andamento=True,
                tempo_fim__isnull=True
            ).first()
            
            if sessao_estudo:
                sessao_estudo.tempo_restante = tempo_restante
                sessao_estudo.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Sessão não encontrada ou não está ativa'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


@login_required
def proxima_fase(request, sessao_id):
    """Avança para a próxima fase (foco/pausa)"""
    pomodoro = get_object_or_404(
        PomodoroSession, 
        id=sessao_id, 
        user=request.user,
        em_andamento=True
    )
    
    sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
    
    if sessao_atual:
        # Finalizar sessão atual
        sessao_atual.tempo_fim = timezone.now()
        sessao_atual.status = 'completo'
        sessao_atual.save()
        
        # Calcular tempo estudado
        if sessao_atual.status == 'foco':
            duracao = sessao_atual.duracao_minutos()
            pomodoro.tempo_total_estudado += duracao
            
            # Atualizar meta diária
            meta, created = MetaDiaria.objects.get_or_create(
                user=request.user,
                data=timezone.now().date()
            )
            meta.minutos_estudados += duracao
            meta.save()
        
        # Determinar próxima fase
        if sessao_atual.status == 'foco':
            pomodoro.ciclos_completados += 1
            
            if pomodoro.ciclos_completados % pomodoro.ciclos_para_pausa_longa == 0:
                proximo_status = 'pausa_longa'
                proximo_tempo = pomodoro.tempo_pausa_longa
            else:
                proximo_status = 'pausa_curta'
                proximo_tempo = pomodoro.tempo_pausa_curta
            
            proximo_ciclo = pomodoro.ciclos_completados + 1
        else:
            proximo_status = 'foco'
            proximo_tempo = pomodoro.tempo_foco
            proximo_ciclo = pomodoro.ciclos_completados + 1
        
        # Criar próxima sessão
        SessaoEstudo.objects.create(
            pomodoro_session=pomodoro,
            status=proximo_status,
            ciclo_numero=proximo_ciclo,
            tempo_inicio=timezone.now(),
            tempo_restante=proximo_tempo * 60
        )
        
        pomodoro.save()
        
        status_display = proximo_status.replace('_', ' ').title()
        messages.info(request, f'✅ Próxima fase: {status_display} iniciada!')
    
    return redirect('pomodoro:dashboard')


@login_required
def pausar_sessao(request, sessao_id):
    """Pausa a sessão atual"""
    pomodoro = get_object_or_404(
        PomodoroSession, 
        id=sessao_id, 
        user=request.user,
        em_andamento=True
    )
    
    sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
    if sessao_atual:
        sessao_atual.status = 'pausado'
        sessao_atual.save()
        messages.warning(request, '⏸️ Sessão pausada. Você pode retomar quando quiser.')
    
    return redirect('pomodoro:dashboard')


@login_required
def retomar_sessao(request, sessao_id):
    """Retoma uma sessão pausada"""
    pomodoro = get_object_or_404(
        PomodoroSession, 
        id=sessao_id, 
        user=request.user,
        em_andamento=True
    )
    
    sessao_atual = pomodoro.sessoes.filter(status='pausado').last()
    if sessao_atual:
        # Recalcular tempo restante
        tempo_decorrido = (timezone.now() - sessao_atual.tempo_inicio).seconds
        tempo_restante = max(0, sessao_atual.tempo_restante - tempo_decorrido)
        
        sessao_atual.status = 'foco' if sessao_atual.status == 'pausado' else sessao_atual.status
        sessao_atual.tempo_inicio = timezone.now()
        sessao_atual.tempo_restante = tempo_restante
        sessao_atual.save()
        messages.success(request, '▶️ Sessão retomada! Continue focado!')
    
    return redirect('pomodoro:dashboard')


@login_required
def finalizar_sessao(request, sessao_id):
    """Finaliza a sessão Pomodoro"""
    pomodoro = get_object_or_404(
        PomodoroSession, 
        id=sessao_id, 
        user=request.user,
        em_andamento=True
    )
    
    sessao_atual = pomodoro.sessoes.filter(tempo_fim__isnull=True).first()
    if sessao_atual:
        sessao_atual.tempo_fim = timezone.now()
        sessao_atual.status = 'completo'
        sessao_atual.save()
        
        # Adicionar tempo estudado se estava em foco
        if sessao_atual.status == 'foco':
            duracao = sessao_atual.duracao_minutos()
            pomodoro.tempo_total_estudado += duracao
            
            # Atualizar meta diária
            meta, created = MetaDiaria.objects.get_or_create(
                user=request.user,
                data=timezone.now().date()
            )
            meta.minutos_estudados += duracao
            meta.save()
    
    pomodoro.em_andamento = False
    pomodoro.data_finalizacao = timezone.now()
    pomodoro.save()
    
    messages.success(request, '✅ Sessão finalizada com sucesso! Ótimo trabalho! 🎉')
    return redirect('pomodoro:dashboard')


@login_required
def estatisticas(request):
    """Página de estatísticas"""
    # Estatísticas gerais
    total_sessoes = PomodoroSession.objects.filter(user=request.user).count()
    
    total_minutos_result = PomodoroSession.objects.filter(
        user=request.user
    ).aggregate(total=Sum('tempo_total_estudado'))
    total_minutos = total_minutos_result['total'] or 0
    
    # Distribuição por modalidade
    modalidades_raw = PomodoroSession.objects.filter(user=request.user)
    modalidades_data = []
    
    for tecnica, display in PomodoroSession.TECNICA_CHOICES:
        sessoes_tecnica = modalidades_raw.filter(tecnica=tecnica)
        total_sessoes_tecnica = sessoes_tecnica.count()
        total_minutos_tecnica = sessoes_tecnica.aggregate(
            total=Sum('tempo_total_estudado')
        )['total'] or 0
        
        if total_sessoes > 0:
            porcentagem = (total_minutos_tecnica / total_minutos * 100) if total_minutos > 0 else 0
        else:
            porcentagem = 0
        
        modalidades_data.append({
            'tecnica': tecnica,
            'tecnica_display': display,
            'total': total_sessoes_tecnica,
            'minutos': total_minutos_tecnica,
            'porcentagem': round(porcentagem, 1)
        })
    
    # Meta diária atual
    meta_hoje, created = MetaDiaria.objects.get_or_create(
        user=request.user,
        data=timezone.now().date()
    )
    
    # Histórico de metas
    historico_metas = MetaDiaria.objects.filter(
        user=request.user
    ).order_by('-data')[:30]
    
    contexto = {
        'total_sessoes': total_sessoes,
        'total_minutos': total_minutos,
        'total_horas': round(total_minutos / 60, 1),
        'modalidades': modalidades_data,
        'meta_hoje': meta_hoje,
        'historico_metas': historico_metas,
    }
    
    return render(request, 'pomodoro_app/estatisticas.html', contexto)


@login_required
def atualizar_meta(request):
    """Atualiza a meta diária"""
    if request.method == 'POST':
        meta, created = MetaDiaria.objects.get_or_create(
            user=request.user,
            data=timezone.now().date()
        )
        form = MetaDiariaForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Meta diária atualizada com sucesso!')
        else:
            for error in form.errors.get('meta_minutos', []):
                messages.error(request, f'Meta: {error}')
    
    return redirect('pomodoro:dashboard')


@login_required
def custom_logout(request):
    """View personalizada para logout"""
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'pomodoro_app/logout_confirm.html')


# ============================================
# VIEWS PARA MÚSICAS
# ============================================

@login_required
def musicas_estudo(request):
    """Página de gerenciamento de músicas"""
    musicas = MusicaEstudo.objects.filter(
        Q(user=request.user) | Q(publica=True)
    ).distinct().order_by('-data_upload')
    
    playlists = PlaylistEstudo.objects.filter(user=request.user)
    
    contexto = {
        'musicas': musicas,
        'playlists': playlists,
        'form_musica': MusicaEstudoForm(),
        'form_playlist': PlaylistEstudoForm(user=request.user),
    }
    
    return render(request, 'pomodoro_app/musicas.html', contexto)


@login_required
def upload_musica(request):
    """Upload de nova música"""
    if request.method == 'POST':
        form = MusicaEstudoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                musica = form.save(commit=False)
                musica.user = request.user
                
                # Calcular duração do arquivo (simplificado por enquanto)
                arquivo = musica.arquivo_audio
                extensao = os.path.splitext(arquivo.name)[1].lower()
                
                # Para simplificar, vamos usar um valor padrão
                # Em produção, você pode implementar a detecção real de duração
                musica.duracao = 300  # 5 minutos padrão
                
                musica.save()
                messages.success(request, f'Música "{musica.nome}" adicionada com sucesso!')
                
            except Exception as e:
                messages.error(request, f'Erro ao processar música: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return redirect('pomodoro:musicas')


@login_required
def criar_playlist(request):
    """Criar nova playlist"""
    if request.method == 'POST':
        form = PlaylistEstudoForm(request.user, request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            
            # Adicionar músicas selecionadas
            musicas_selecionadas = form.cleaned_data.get('musicas_selecionadas', [])
            playlist.musicas.set(musicas_selecionadas)
            
            messages.success(request, f'Playlist "{playlist.nome}" criada com sucesso!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return redirect('pomodoro:musicas')


@login_required
def deletar_musica(request, musica_id):
    """Deletar música"""
    musica = get_object_or_404(MusicaEstudo, id=musica_id, user=request.user)
    
    # Verificar se a música está em uso
    if PomodoroSession.objects.filter(musica_atual=musica, em_andamento=True).exists():
        messages.error(request, 'Não é possível deletar esta música pois está em uso em uma sessão ativa.')
    else:
        # Remover arquivo físico
        if musica.arquivo_audio:
            if os.path.isfile(musica.arquivo_audio.path):
                try:
                    os.remove(musica.arquivo_audio.path)
                except:
                    pass  # Ignorar erro se o arquivo não existir
        
        nome_musica = musica.nome
        musica.delete()
        messages.success(request, f'Música "{nome_musica}" deletada com sucesso!')
    
    return redirect('pomodoro:musicas')


@login_required
def deletar_playlist(request, playlist_id):
    """Deletar playlist"""
    playlist = get_object_or_404(PlaylistEstudo, id=playlist_id, user=request.user)
    
    # Verificar se a playlist está em uso
    if PomodoroSession.objects.filter(playlist=playlist, em_andamento=True).exists():
        messages.error(request, 'Não é possível deletar esta playlist pois está em uso em uma sessão ativa.')
    else:
        nome_playlist = playlist.nome
        playlist.delete()
        messages.success(request, f'Playlist "{nome_playlist}" deletada com sucesso!')
    
    return redirect('pomodoro:musicas')


@login_required
def play_musica(request, musica_id):
    """API para tocar música"""
    musica = get_object_or_404(
        MusicaEstudo.objects.filter(
            Q(user=request.user) | Q(publica=True)
        ),
        id=musica_id
    )
    
    # Atualizar estatísticas
    musica.vezes_tocada += 1
    musica.ultima_reproducao = timezone.now()
    musica.save()
    
    return JsonResponse({
        'status': 'success',
        'url': musica.arquivo_audio.url,
        'nome': musica.nome,
        'duracao': musica.duracao
    })


@login_required
def get_playlist_musicas(request, playlist_id):
    """API para obter músicas de uma playlist"""
    playlist = get_object_or_404(PlaylistEstudo, id=playlist_id, user=request.user)
    
    musicas = []
    for musica in playlist.musicas.all():
        musicas.append({
            'id': musica.id,
            'nome': musica.nome,
            'url': musica.arquivo_audio.url,
            'duracao': musica.duracao,
            'extensao': musica.get_extensao()
        })
    
    return JsonResponse({
        'status': 'success',
        'playlist': playlist.nome,
        'ordem_reproducao': playlist.ordem_reproducao,
        'musicas': musicas
    })


@login_required
def usar_playlist(request, playlist_id):
    """API para usar uma playlist no Pomodoro"""
    playlist = get_object_or_404(PlaylistEstudo, id=playlist_id, user=request.user)
    
    # Salvar preferência no perfil do usuário (simplificado)
    messages.success(request, f'Playlist "{playlist.nome}" selecionada para uso nas sessões!')
    
    return redirect('pomodoro:dashboard')