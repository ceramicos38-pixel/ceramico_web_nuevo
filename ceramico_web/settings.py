from pathlib import Path
from decimal import Decimal
import os
import dj_database_url

# -----------------------------
# BASE DEL PROYECTO
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# CONSTANTES ADICIONALES
# -----------------------------
TAX_RATE = Decimal('0.18')  # IGV = 18%
TOMISOFT_URL = 'https://admin.tumi-soft.com/admin/sales/v2/vouchers'
TOMISOFT_METHOD = 'POST'
TOMISOFT_API_KEY = os.getenv("TOMISOFT_API_KEY", "")

# -----------------------------
# CONFIGURACIÓN DE SEGURIDAD
# -----------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'evelyn2025')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,ceramico-web.onrender.com"
).split(",")

if "RENDER_EXTERNAL_HOSTNAME" in os.environ:
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])

# -----------------------------
# APLICACIONES INSTALADAS
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones propias
    'inventario',

    # Terceros
    'widget_tweaks',
]

# -----------------------------
# MIDDLEWARE
# -----------------------------
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

# -----------------------------
# URLs Y WSGI
# -----------------------------
ROOT_URLCONF = 'ceramico_web.urls'
WSGI_APPLICATION = 'ceramico_web.wsgi.application'

# -----------------------------
# TEMPLATES
# -----------------------------
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

# -----------------------------
# BASE DE DATOS
# -----------------------------
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -----------------------------
# VALIDACIÓN DE CONTRASEÑAS
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# LOCALIZACIÓN
# -----------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC & MEDIA
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]  # donde están tus archivos originales
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------
# LOGIN/LOGOUT
# -----------------------------
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# -----------------------------
# AJUSTES ADICIONALES
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
