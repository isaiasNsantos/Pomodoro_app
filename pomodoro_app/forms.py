# pomodoro_app/forms.py - VERSÃO COMPLETA E SIMPLIFICADA
from django import forms
from django.db.models import Q
from .models import PomodoroSession, MetaDiaria, MusicaEstudo, PlaylistEstudo
import os

# ============================================
# FORMULÁRIOS DO POMODORO
# ============================================

class PomodoroSessionForm(forms.ModelForm):
    class Meta:
        model = PomodoroSession
        fields = [
            'tecnica', 'modalidade', 
            'tempo_foco', 'tempo_pausa_curta', 'tempo_pausa_longa', 'ciclos_para_pausa_longa',
            'som_notificacao', 'notificacao_desktop',
            'tocar_musica', 'volume_musica', 'playlist', 'loop_musica'
        ]
        
        widgets = {
            'tecnica': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_tecnica'
            }),
            'modalidade': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_modalidade'
            }),
            'tempo_foco': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '120',
                'id': 'id_tempo_foco',
                'placeholder': '25'
            }),
            'tempo_pausa_curta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '30',
                'id': 'id_tempo_pausa_curta',
                'placeholder': '5'
            }),
            'tempo_pausa_longa': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '5',
                'max': '60',
                'id': 'id_tempo_pausa_longa',
                'placeholder': '15'
            }),
            'ciclos_para_pausa_longa': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20',
                'id': 'id_ciclos_para_pausa_longa',
                'placeholder': '4'
            }),
            'som_notificacao': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_som_notificacao'
            }),
            'notificacao_desktop': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_notificacao_desktop'
            }),
            'tocar_musica': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_tocar_musica'
            }),
            'volume_musica': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'id': 'id_volume_musica',
                'value': '50'
            }),
            'playlist': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_playlist'
            }),
            'loop_musica': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_loop_musica'
            }),
        }
        
        labels = {
            'tecnica': 'Técnica',
            'modalidade': 'Modalidade de Estudo',
            'tempo_foco': 'Tempo de Foco (minutos)',
            'tempo_pausa_curta': 'Tempo de Pausa Curta (minutos)',
            'tempo_pausa_longa': 'Tempo de Pausa Longa (minutos)',
            'ciclos_para_pausa_longa': 'Ciclos para Pausa Longa',
            'som_notificacao': 'Som de Notificação',
            'notificacao_desktop': 'Notificação na Área de Trabalho',
            'tocar_musica': 'Tocar Música durante o Estudo',
            'volume_musica': 'Volume da Música (0-100)',
            'playlist': 'Playlist para Estudo',
            'loop_musica': 'Repetir Música (Loop)',
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filtrar playlists do usuário
            self.fields['playlist'].queryset = PlaylistEstudo.objects.filter(user=user)
        
        # Definir valores iniciais
        self.fields['volume_musica'].initial = 50
        self.fields['tocar_musica'].initial = False
        self.fields['loop_musica'].initial = False
        self.fields['playlist'].required = False  # Tornar opcional
    
    def clean_tempo_foco(self):
        tempo_foco = self.cleaned_data.get('tempo_foco')
        if tempo_foco is None or tempo_foco < 1 or tempo_foco > 120:
            raise forms.ValidationError('O tempo de foco deve estar entre 1 e 120 minutos.')
        return tempo_foco
    
    def clean_tempo_pausa_curta(self):
        tempo_pausa_curta = self.cleaned_data.get('tempo_pausa_curta')
        if tempo_pausa_curta is None or tempo_pausa_curta < 1 or tempo_pausa_curta > 30:
            raise forms.ValidationError('O tempo de pausa curta deve estar entre 1 e 30 minutos.')
        return tempo_pausa_curta
    
    def clean_tempo_pausa_longa(self):
        tempo_pausa_longa = self.cleaned_data.get('tempo_pausa_longa')
        if tempo_pausa_longa is None or tempo_pausa_longa < 5 or tempo_pausa_longa > 60:
            raise forms.ValidationError('O tempo de pausa longa deve estar entre 5 e 60 minutos.')
        return tempo_pausa_longa
    
    def clean_ciclos_para_pausa_longa(self):
        ciclos = self.cleaned_data.get('ciclos_para_pausa_longa')
        if ciclos is None or ciclos < 1 or ciclos > 20:
            raise forms.ValidationError('Os ciclos para pausa longa devem estar entre 1 e 20.')
        return ciclos
    
    def clean_volume_musica(self):
        volume = self.cleaned_data.get('volume_musica')
        if volume is None:
            return 50  # Valor padrão
        if volume < 0 or volume > 100:
            raise forms.ValidationError('O volume deve estar entre 0 e 100.')
        return volume


class MetaDiariaForm(forms.ModelForm):
    class Meta:
        model = MetaDiaria
        fields = ['meta_minutos']
        widgets = {
            'meta_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'max': '480',
                'id': 'id_meta_minutos'
            }),
        }
        labels = {
            'meta_minutos': 'Meta Diária (minutos)',
        }
    
    def clean_meta_minutos(self):
        meta_minutos = self.cleaned_data.get('meta_minutos')
        if meta_minutos < 15:
            raise forms.ValidationError('A meta diária deve ser de pelo menos 15 minutos.')
        if meta_minutos > 480:
            raise forms.ValidationError('A meta diária não pode exceder 480 minutos (8 horas).')
        return meta_minutos


# ============================================
# FORMULÁRIOS PARA MÚSICAS
# ============================================

class MusicaEstudoForm(forms.ModelForm):
    class Meta:
        model = MusicaEstudo
        fields = ['nome', 'descricao', 'arquivo_audio', 'publica', 'tags']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da música'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição (opcional)'
            }),
            'arquivo_audio': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.mp3,.wav,.ogg,.m4a'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'estudo, foco, relaxante, instrumental'
            }),
            'publica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nome': 'Nome da Música',
            'descricao': 'Descrição',
            'arquivo_audio': 'Arquivo de Áudio',
            'publica': 'Tornar pública',
            'tags': 'Tags (separadas por vírgula)',
        }
    
    def clean_arquivo_audio(self):
        arquivo = self.cleaned_data.get('arquivo_audio')
        
        if arquivo:
            # Validar extensão
            extensao = os.path.splitext(arquivo.name)[1].lower()
            extensoes_validas = ['.mp3', '.wav', '.ogg', '.m4a']
            
            if extensao not in extensoes_validas:
                raise forms.ValidationError(
                    f'Tipo de arquivo não suportado. Use: {", ".join(extensoes_validas)}'
                )
            
            # Validar tamanho (50MB)
            tamanho_maximo = 50 * 1024 * 1024  # 50MB
            if arquivo.size > tamanho_maximo:
                raise forms.ValidationError(
                    f'Arquivo muito grande. Tamanho máximo: 50MB'
                )
        
        return arquivo
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome or len(nome.strip()) < 2:
            raise forms.ValidationError('O nome da música deve ter pelo menos 2 caracteres.')
        return nome.strip()


class PlaylistEstudoForm(forms.ModelForm):
    musicas_selecionadas = forms.ModelMultipleChoiceField(
        queryset=MusicaEstudo.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Selecionar Músicas'
    )
    
    class Meta:
        model = PlaylistEstudo
        fields = ['nome', 'descricao', 'ordem_reproducao', 'cor_fundo', 'icone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da playlist'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da playlist'
            }),
            'ordem_reproducao': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cor_fundo': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icone': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'nome': 'Nome da Playlist',
            'descricao': 'Descrição',
            'ordem_reproducao': 'Ordem de Reprodução',
            'cor_fundo': 'Cor de Fundo',
            'icone': 'Ícone',
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filtrar músicas do usuário e públicas
            self.fields['musicas_selecionadas'].queryset = MusicaEstudo.objects.filter(
                Q(user=user) | Q(publica=True)
            ).distinct()
        
        # Opções de ícones
        ICONE_CHOICES = [
            ('fas fa-music', '🎵 Música'),
            ('fas fa-headphones', '🎧 Fones'),
            ('fas fa-guitar', '🎸 Guitarra'),
            ('fas fa-piano', '🎹 Piano'),
            ('fas fa-drum', '🥁 Bateria'),
            ('fas fa-brain', '🧠 Cérebro'),
            ('fas fa-book', '📚 Livro'),
            ('fas fa-star', '⭐ Estrela'),
            ('fas fa-heart', '❤️ Coração'),
        ]
        self.fields['icone'].widget.choices = ICONE_CHOICES
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome or len(nome.strip()) < 2:
            raise forms.ValidationError('O nome da playlist deve ter pelo menos 2 caracteres.')
        return nome.strip()