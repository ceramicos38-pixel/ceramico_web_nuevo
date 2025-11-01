from django.apps import AppConfig
from django.conf import settings

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        # Solo crear superusuario en Render
        if settings.DEBUG is False and settings.RENDER:
            from django.contrib.auth.models import User
            try:
                if not User.objects.filter(username="ADMIN").exists():
                    User.objects.create_superuser(
                        username="ADMIN",
                        email="admin@ceramico.com",
                        password="evelyn2025"
                    )
                    print("✅ Superusuario creado automáticamente")
            except:
                pass
