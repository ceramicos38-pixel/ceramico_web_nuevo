# ceramico_web/urls.py (archivo del proyecto principal)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),  # nuestra app de inventario/cerámicos
]
