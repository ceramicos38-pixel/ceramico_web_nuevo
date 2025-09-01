from django import forms
from .models import Producto, Categoria, Cliente, Sale, SaleItem
from decimal import Decimal

# --------------------------
# FORMULARIO PRODUCTO
# --------------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # ✅ Solo dejamos los campos que realmente existen en el modelo
        fields = ['nombre', 'marca', 'categoria', 'stock', 'unidad_medida', 'precio_venta', 'proveedor']
        labels = {
            'nombre': 'Nombre',
            'marca': 'Marca',
            'categoria': 'Categoría',
            'stock': 'Stock',
            'unidad_medida': 'U.M.',
            'precio_venta': 'Precio de Venta (S/)',
            'proveedor': 'Proveedor',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cemento Portland'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Sol'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-control'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ferretería San Juan'
            }),
        }

# --------------------------
# FORMULARIO VENTA
# --------------------------
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['cliente', 'tipo_comprobante']  # el total se calcula solo

# --------------------------
# FORMULARIO ITEM DE VENTA
# --------------------------
class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
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
