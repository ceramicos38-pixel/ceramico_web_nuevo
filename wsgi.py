"""
WSGI config for ceramico_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramico_web.settings')

from django.core.wsgi import get_wsgi_application

# Crear superusuario automáticamente (solo si no existe)
try:
    import ceramico_web.create_superuser
except Exception as e:
    # No interrumpir el deploy si hay un error
    import sys
    print(f"⚠️ Error al crear superusuario: {e}", file=sys.stderr)

application = get_wsgi_application()
