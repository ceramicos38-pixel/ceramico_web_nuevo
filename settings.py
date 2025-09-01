from pathlib import Path
from decimal import Decimal
import os

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Constantes adicionales
TAX_RATE = Decimal('0.18')   # IGV = 18%
SMARTCLICK_URL = 'https://your-smartclick-url.example/emit'
SMARTCLICK_METHOD = 'GET'
SMARTCLICK_API_KEY = ''

# Clave secreta (⚠️ en producción lo ideal es usar variables de entorno)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'evelyn2025')

# Debug desactivado en producción
DEBUG = 'True'

# Hosts permitidos (Render + PythonAnywhere + local)
ALLOWED_HOSTS = [
    'EVELYNADMIN.pythonanywhere.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1'
]

# Aplicaciones instaladas
INSTALLED_APPS = [
    # apps de Django
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
        'DIRS': [BASE_DIR / 'templates'],  # carpeta templates en raíz
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

# Base de datos (SQLite por ahora, en Render se puede cambiar a PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Limite para carga masiva de Excel/CSV
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] # tus archivos en /static
STATIC_ROOT = BASE_DIR / "staticfiles"    # carpeta donde se recopilan al hacer collectstatic
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración adicional
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rutas de login/logout
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'
