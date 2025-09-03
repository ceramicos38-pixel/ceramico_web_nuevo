import django
from django.contrib.auth.models import User
from django.db import OperationalError

try:
    if not User.objects.filter(username="ADMIN").exists():
        User.objects.create_superuser(
            username="ADMIN",
            email="admin@ceramico.com",
            password="evelyn2025"
        )
        print("✅ Superusuario creado automáticamente")
except OperationalError:
    # Esto ocurre si la DB aún no tiene migraciones
    print("⚠️ Base de datos aún no lista, no se creó el superusuario")
