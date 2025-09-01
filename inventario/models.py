from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Sum, F, FloatField

# ========================
# CAJA
# ========================
class Caja(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    abierta = models.BooleanField(default=True)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Caja de {self.usuario.username} - {self.fecha_apertura.date()}"


# ========================
# CLIENTE
# ========================
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


# ========================
# CATEGORÍA
# ========================
class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ========================
# PRODUCTO (Cerámicos)
# ========================
class Producto(models.Model):
    UNIDADES = [
        ("caja", "Caja"),
        ("m2", "Metro cuadrado"),
        ("unidad", "Unidad"),
    ]

    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES, default="caja")
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendidos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Nos aseguramos que los decimales estén limpios
        self.precio_venta = Decimal(self.precio_venta or 0)
        self.stock = Decimal(self.stock or 0)
        self.vendidos = Decimal(self.vendidos or 0)

        # Ya no calculamos nada extra (sin ganancia, sin inversión)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - {self.stock} {self.unidad_medida}"



# ========================
# VENTAS
# ========================
class Sale(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    tipo_comprobante = models.CharField(
        max_length=50,
        choices=[
            ("Nota", "Nota de Venta"),
            ("Boleta", "Boleta"),
            ("Factura", "Factura"),
        ]
    )
    fecha = models.DateTimeField(auto_now_add=True)
    numero_venta = models.PositiveIntegerField(unique=True, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    caja = models.ForeignKey("Caja", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Número de venta consecutivo
        if not self.numero_venta:
            last_sale = Sale.objects.order_by('-numero_venta').first()
            self.numero_venta = 1 if not last_sale else last_sale.numero_venta + 1

        is_new = self.pk is None
        previous_total = Decimal("0.00")
        previous_caja = None

        if not is_new:
            prev = Sale.objects.get(pk=self.pk)
            previous_total = prev.total
            previous_caja = prev.caja

        if is_new:
            super().save(*args, **kwargs)

        # Calcular total desde items
        total_calculado = self.items.aggregate(
            total=Sum(F('cantidad') * F('precio'), output_field=FloatField())
        )['total'] or 0
        self.total = Decimal(str(total_calculado))

        # Asociar a caja abierta
        if not self.caja:
            caja_abierta = Caja.objects.filter(abierta=True).first()
            if caja_abierta:
                self.caja = caja_abierta

        super().save(update_fields=['total', 'caja'])

        # Ajustar caja
        if self.caja and self.caja.abierta:
            if self.caja.total is None:
                self.caja.total = Decimal("0.00")

            if is_new:
                self.caja.total += self.total
            else:
                if previous_caja == self.caja:
                    self.caja.total = self.caja.total - previous_total + self.total
                else:
                    if previous_caja:
                        previous_caja.total = (previous_caja.total or 0) - previous_total
                        previous_caja.save(update_fields=['total'])
                    self.caja.total += self.total

            self.caja.save(update_fields=['total'])

    def __str__(self):
        return f"Venta #{self.numero_venta} - {self.cliente}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)  # decimal por cajas/m²
    precio = models.DecimalField(max_digits=12, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

    def save(self, *args, **kwargs):
        # Si no se envía precio, se toma el de producto
        if not self.precio and hasattr(self.producto, "precio_venta"):
            self.precio = self.producto.precio_venta
        super().save(*args, **kwargs)

        # Recalcular total de la venta
        if self.sale_id:
            self.sale.save()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} {self.producto.unidad_medida}"
