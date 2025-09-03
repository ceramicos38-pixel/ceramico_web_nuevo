import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramico_web.settings')
django.setup()

username = "ADMIN"
email = "admin@ceramico.com"
password = "evelyn2025"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superusuario creado automáticamente")
