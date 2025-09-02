# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceramico_web.settings')
django.setup()

from django.contrib.auth.models import User

username = 'EVELYNADMIN'
email = 'ceramicos38@gmail.com'
password = 'evelyn123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuario {username} creado correctamente")
else:
    print(f"Superusuario {username} ya existe")
