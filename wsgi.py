"""
WSGI config for ceramico_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Ejecutar script de superusuario automáticamente
script_path = os.path.join(os.path.dirname(__file__), 'create_superuser.py')
if os.path.exists(script_path):
    import runpy
    runpy.run_path(script_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramico_web.settings')

application = get_wsgi_application()
