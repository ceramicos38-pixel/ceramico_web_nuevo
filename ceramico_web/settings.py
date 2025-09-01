from pathlib import Path
from decimal import Decimal
import os
import dj_database_url

# --------------------------
# BASE DEL PROYECTO
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# CONSTANTES ADICIONALES
# --------------------------
TAX_RATE = Decimal('0.18')  # IGV = 18%
SMARTCLICK_URL = 'https://your-smartclick-url.example/emit'
SMARTCLICK_METHOD = 'GET'
SMARTCLICK_API_KEY = ''

# --------------------------
# CLAVE SECRETA Y DEBUG
# --------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'evelyn2025')
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# --------------------------
# HOSTS PERMITIDOS
# --------------------------
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# --------------------------
# APLICACIONES INSTALADAS
# --------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tu app
    'inventario',

    # terceros
    'widget_tweaks',
]

# --------------------------
# MIDDLEWARE
# --------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------
# URLS Y WSGI
# --------------------------
ROOT_URLCONF = 'ceramico_web.urls'
WSGI_APPLICATION = 'ceramico_web.wsgi.application'

# --------------------------
# TEMPLATES
# --------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# --------------------------
# BASE DE DATOS (Render/PostgreSQL)
# --------------------------
# BASE DE DATOS
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False  # solo para SQLite local
    )
}


# --------------------------
# VALIDACIÓN DE CONTRASEÑAS
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------
# LOCALIZACIÓN
# --------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# --------------------------
# ARCHIVOS ESTÁTICOS
# --------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# ARCHIVOS MEDIA
# --------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------
# CONFIGURACIÓN ADICIONAL
# --------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------
# LOGIN / LOGOUT
# --------------------------
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# --------------------------
# LÍMITE PARA SUBIDAS MASIVAS
# --------------------------
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
