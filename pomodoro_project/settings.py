# # pomodoro_project/settings.py

# import os
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'sua-chave-secreta-aqui'

# DEBUG = True

# ALLOWED_HOSTS = []

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'pomodoro_app',  # Nosso app
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'pomodoro_project.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             os.path.join(BASE_DIR, 'templates'),
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'pomodoro_project.wsgi.application'

# # Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'pt-br'
# TIME_ZONE = 'America/Sao_Paulo'
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Login redirect
# LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = '/accounts/login/'

# LOGOUT_REDIRECT_URL = '/'

# # Configurações de mídia
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Tamanho máximo de upload (50MB)
# FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
# DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

# # Extensões permitidas para áudio
# AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.m4a']


# pomodoro_project/settings.py

import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='sua-chave-secreta-aqui')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pomodoro_app',  # Nosso app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pomodoro_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pomodoro_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = config('STATIC_URL', default='static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login redirect
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'

# Configurações de mídia
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tamanho máximo de upload (50MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Extensões permitidas para áudio
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.m4a']

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# Custom Pomodoro settings
DEFAULT_POMODORO_MINUTES = config('DEFAULT_POMODORO_MINUTES', default=25, cast=int)
DEFAULT_SHORT_BREAK_MINUTES = config('DEFAULT_SHORT_BREAK_MINUTES', default=5, cast=int)
DEFAULT_LONG_BREAK_MINUTES = config('DEFAULT_LONG_BREAK_MINUTES', default=15, cast=int)
POMODOROS_PER_SET = config('POMODOROS_PER_SET', default=4, cast=int)