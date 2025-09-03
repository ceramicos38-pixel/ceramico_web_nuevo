from django.urls import path, include

urlpatterns = [
    path('', include('inventario.urls')),  # todas las rutas en inventario
]
