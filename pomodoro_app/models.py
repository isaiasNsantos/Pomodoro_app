from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.storage import FileSystemStorage
import os

# ============================================
# MODELOS PRINCIPAIS DO POMODORO
# ============================================

class PomodoroSession(models.Model):
    """Sessão de estudo Pomodoro"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    
    TECNICA_CHOICES = [
        ('pomodoro', 'Técnica Pomodoro Clássica'),
        ('personalizado', 'Técnica Personalizada'),
    ]
    
    MODALIDADE_CHOICES = [
        ('foco', 'Foco Total'),
        ('revisao', 'Revisão'),
        ('pratica', 'Prática'),
        ('leitura', 'Leitura'),
    ]
    
    tecnica = models.CharField(max_length=20, choices=TECNICA_CHOICES, default='pomodoro')
    modalidade = models.CharField(max_length=20, choices=MODALIDADE_CHOICES, default='foco')
    
    # Tempos em minutos
    tempo_foco = models.IntegerField(
        default=25, 
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    tempo_pausa_curta = models.IntegerField(
        default=5, 
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    tempo_pausa_longa = models.IntegerField(
        default=15, 
        validators=[MinValueValidator(5), MaxValueValidator(60)]
    )
    ciclos_para_pausa_longa = models.IntegerField(
        default=4, 
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    
    # Status da sessão
    ciclos_completados = models.IntegerField(default=0)
    tempo_total_estudado = models.IntegerField(default=0)  # Em minutos
    em_andamento = models.BooleanField(default=False)
    
    # Configurações de notificação
    som_notificacao = models.BooleanField(default=True)
    notificacao_desktop = models.BooleanField(default=True)
    
    # Configurações de áudio (NOVOS CAMPOS)
    tocar_musica = models.BooleanField(default=False)
    volume_musica = models.IntegerField(
        default=50, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    loop_musica = models.BooleanField(default=False)
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Pomodoro de {self.user.username} - {self.get_tecnica_display()}"
    
    def get_modality_display(self):
        """Retorna o display da modalidade"""
        for choice in self.MODALIDADE_CHOICES:
            if choice[0] == self.modalidade:
                return choice[1]
        return self.modalidade


class SessaoEstudo(models.Model):
    """Registro individual de cada sessão de estudo"""
    pomodoro_session = models.ForeignKey(PomodoroSession, on_delete=models.CASCADE, related_name='sessoes')
    
    STATUS_CHOICES = [
        ('foco', 'Em Foco'),
        ('pausa_curta', 'Pausa Curta'),
        ('pausa_longa', 'Pausa Longa'),
        ('completo', 'Completo'),
        ('pausado', 'Pausado'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='foco')
    ciclo_numero = models.IntegerField(default=1)
    
    # Tempos
    tempo_inicio = models.DateTimeField()
    tempo_fim = models.DateTimeField(null=True, blank=True)
    tempo_restante = models.IntegerField()  # Em segundos
    
    # Métricas
    distracoes = models.IntegerField(default=0)
    notas = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-tempo_inicio']
    
    def duracao_minutos(self):
        if self.tempo_fim:
            duracao = (self.tempo_fim - self.tempo_inicio).seconds // 60
            return duracao
        return 0


class MetaDiaria(models.Model):
    """Metas diárias de estudo"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_diarias')
    data = models.DateField(default=timezone.now)
    meta_minutos = models.IntegerField(default=120)
    minutos_estudados = models.IntegerField(default=0)
    concluida = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'data']
        ordering = ['-data']
    
    def progresso_porcentagem(self):
        if self.meta_minutos > 0:
            return min(100, (self.minutos_estudados / self.meta_minutos) * 100)
        return 0


# ============================================
# MODELOS PARA MÚSICAS
# ============================================

# Configurar armazenamento de músicas
musicas_storage = FileSystemStorage(location='media/musicas/')

from django.core.validators import FileExtensionValidator

class MusicaEstudo(models.Model):
    """Modelo para armazenar músicas de estudo personalizadas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musicas_estudo')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    arquivo_audio = models.FileField(
        upload_to='musicas/',
        storage=musicas_storage,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg', 'm4a'])
        ]
    )
    duracao = models.IntegerField(default=0, help_text="Duração em segundos")
    publica = models.BooleanField(default=False, help_text="Disponível para outros usuários")
    tags = models.CharField(max_length=200, blank=True, help_text="Tags separadas por vírgula")
    
    # Estatísticas
    vezes_tocada = models.IntegerField(default=0)
    data_upload = models.DateTimeField(auto_now_add=True)
    ultima_reproducao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-data_upload']
    
    def __str__(self):
        return f"{self.nome} - {self.user.username}"
    
    def get_extensao(self):
        return os.path.splitext(self.arquivo_audio.name)[1].lower()
    
    def get_tamanho_mb(self):
        try:
            size = self.arquivo_audio.size
            return round(size / (1024 * 1024), 2)
        except:
            return 0


class PlaylistEstudo(models.Model):
    """Playlists de músicas para estudo"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists_estudo')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    musicas = models.ManyToManyField(MusicaEstudo, related_name='playlists', blank=True)
    ordem_reproducao = models.CharField(
        max_length=20,
        choices=[
            ('sequencial', 'Sequencial'),
            ('aleatoria', 'Aleatória'),
            ('repetir', 'Repetir Única'),
        ],
        default='sequencial'
    )
    cor_fundo = models.CharField(max_length=7, default='#3498db', help_text="Cor em hex (#RRGGBB)")
    icone = models.CharField(max_length=50, default='fas fa-music')
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.user.username}"
    
    def total_duracao(self):
        total = sum(musica.duracao for musica in self.musicas.all())
        minutos = total // 60
        segundos = total % 60
        return f"{minutos}:{segundos:02d}"


# ============================================
# ATUALIZAR RELACIONAMENTOS
# ============================================

# Adicionar campos de relacionamento ao PomodoroSession
PomodoroSession.add_to_class('playlist', models.ForeignKey(
    PlaylistEstudo, 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True,
    related_name='sessoes_pomodoro'
))

PomodoroSession.add_to_class('musica_atual', models.ForeignKey(
    MusicaEstudo,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='sessoes_ativas'
))