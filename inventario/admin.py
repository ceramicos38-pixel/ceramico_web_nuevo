from django.contrib import admin
from .models import Producto, Categoria, Cliente, Caja, Sale, SaleItem

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'stock', 'unidad_medida', 'precio_venta', 'proveedor')
    readonly_fields = ('id',)  # si quieres mostrar el ID nada más

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento')

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'monto_inicial', 'monto_cierre', 'abierta', 'fecha_apertura', 'fecha_cierre', 'total')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'cliente', 'tipo_comprobante', 'fecha', 'total', 'caja')
    inlines = [SaleItemInline]
