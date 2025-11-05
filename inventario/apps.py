from django.apps import AppConfig
from django.conf import settings

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        # Crear superusuario en Render automáticamente
        if not settings.DEBUG and settings.ALLOWED_HOSTS:
            try:
                from django.contrib.auth.models import User
                if not User.objects.filter(username="admin").exists():
                    User.objects.create_superuser(
                        username="admin",
                        email="admin@ceramico.com",
                        password="evelyn2025"
                    )
                    print("✅ Superusuario creado automáticamente en Render (admin / evelyn2025)")
            except Exception as e:
                print("⚠️ Error creando usuario admin en Render:", e)
