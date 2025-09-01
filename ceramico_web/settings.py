from pathlib import Path
from decimal import Decimal
import os
import dj_database_url

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Constantes adicionales
TAX_RATE = Decimal('0.18')  # IGV = 18%
TOMISOFT_URL = 'https://admin.tumi-soft.com/admin/sales/v2/vouchers'
TOMISOFT_METHOD = 'POST'  # si vas a enviar datos
TOMISOFT_API_KEY = os.getenv("TOMISOFT_API_KEY", "")


# Clave secreta
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'evelyn2025')

# Debug desactivado en producción
DEBUG = 'False'

# Hosts permitidos
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", 
    "localhost,127.0.0.1,ceramico-web.onrender.com"
).split(",")


# Aplicaciones instaladas
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

# Middleware
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

# URLs
ROOT_URLCONF = 'ceramico_web.urls'

# Templates
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

# WSGI
WSGI_APPLICATION = 'ceramico_web.wsgi.application'

# Base de datos PostgreSQL (Render)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}


# Límite para carga masiva de Excel/CSV
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos media (subidas de usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Configuración adicional
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rutas de login/logout
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# Configuración para Render
if "RENDER_EXTERNAL_HOSTNAME" in os.environ:
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])
