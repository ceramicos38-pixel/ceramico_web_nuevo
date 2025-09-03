"""
WSGI config for ceramico_web project.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramico_web.settings')

# Inicializa Django primero
application = get_wsgi_application()

# Ahora sí: ejecutar creación de superusuario
try:
    import ceramico_web.create_superuser
except Exception as e:
    print(f"⚠️ Error al crear superusuario: {e}", file=sys.stderr)
