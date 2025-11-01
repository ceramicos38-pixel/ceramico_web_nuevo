from django import forms
from .models import Producto, Categoria, Cliente, Venta, DetalleVenta
from decimal import Decimal

# --------------------------
# FORMULARIO PRODUCTO
# --------------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Todos los campos salvo 'vendidos'
        fields = [
            'nombre',
            'marca',
            'categoria',
            'unidad_medida',
            'precio_venta',
            'stock',
            'proveedor'
        ]
        labels = {
            'nombre': 'Nombre',
            'marca': 'Marca',
            'categoria': 'Categoría',
            'unidad_medida': 'Formato / U.M.',
            'precio_venta': 'Precio de Venta (S/)',
            'stock': 'Stock',
            'proveedor': 'Proveedor',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Anillo de cera'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Magnum'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Unidad, kg, m2, 30x60'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Ej: 25.50'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
                'placeholder': 'Ej: 10'
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Nombre del proveedor'
            }),
        }


# --------------------------
# FORMULARIO VENTA
# --------------------------
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'tipo_comprobante']  # el total se calcula solo

# --------------------------
# FORMULARIO ITEM DE VENTA
# --------------------------
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar nombre, marca, stock y precio de venta
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = (
            lambda obj: f"{obj.nombre} | {obj.marca} | Stock: {obj.stock} | Precio: {obj.precio_venta}"
        )

        # Precio editable
        self.fields['precio'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01'
        })

        # Cantidad editable
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})

# inventario/forms.py

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nueva categoría'}),
        }
