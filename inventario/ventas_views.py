from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory, inlineformset_factory
from django.urls import reverse
from django.contrib import messages
from .forms import ProductoForm, SaleForm, SaleItemForm
from .models import Producto, Categoria, Cliente, Sale, SaleItem, Caja
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# -----------------------------
# Caja
# -----------------------------
@login_required
def abrir_caja(request):
    if request.method == 'POST':
        monto_inicial = request.POST.get('monto_inicial')
        if monto_inicial:
            Caja.objects.create(
                usuario=request.user,
                monto_inicial=Decimal(monto_inicial),
                abierta=True,
                fecha_apertura=timezone.now()
            )
            return redirect('listar_ventas')
        else:
            messages.error(request, "Debes ingresar el monto inicial")
    return render(request, 'inventario/abrir_caja.html')


@login_required
def cerrar_caja(request, caja_id):
    caja = get_object_or_404(Caja, id=caja_id)
    if request.method == "POST":
        monto_cierre = request.POST.get('monto_cierre')
        caja.monto_cierre = Decimal(monto_cierre)
        caja.fecha_cierre = timezone.now()
        caja.abierta = False
        caja.save()
        return redirect('historial_caja')
    return render(request, 'inventario/cerrar_caja.html', {'caja': caja})


@login_required
def historial_caja(request):
    cajas = Caja.objects.all().order_by('-fecha_apertura')
    return render(request, 'inventario/historial_caja.html', {'cajas': cajas})


@login_required
def cerrar_caja_periodo(request, periodo, valor):
    if periodo == "dia":
        ventas = Sale.objects.filter(fecha__date=valor)
    elif periodo == "mes":
        year, month = valor.split("-")
        ventas = Sale.objects.filter(fecha__year=year, fecha__month=month)
    elif periodo == "anio":
        ventas = Sale.objects.filter(fecha__year=valor)
    else:
        ventas = Sale.objects.none()

    total = ventas.aggregate(Sum("total"))["total"] or 0

    # Crear caja de resumen
    Caja.objects.create(
        usuario=request.user,
        fecha_apertura=now(),
        fecha_cierre=now(),
        monto_inicial=0,
        monto_cierre=total,
        abierta=True
    )

    messages.success(request, f"Caja del {periodo} {valor} cerrada con total {total}")
    return redirect("historial_caja")


# -----------------------------
# Ventas
# -----------------------------
SaleForm = modelform_factory(Sale, fields=['cliente', 'tipo_comprobante'])
SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    fields=('producto', 'cantidad', 'precio'),
    extra=1,
    can_delete=True
)


@login_required
def listar_ventas(request):
    ventas = Sale.objects.all().order_by('-fecha')

    # Filtros por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, "%Y-%m-%d"))
        ventas = ventas.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, "%Y-%m-%d"))
        ventas = ventas.filter(fecha__lte=fecha_fin)

    caja_abierta = Caja.objects.filter(abierta=True).first()

    return render(request, 'inventario/listar_ventas.html', {
        'ventas': ventas,
        'caja_abierta': caja_abierta
    })


@login_required
def registrar_venta(request):
    productos = Producto.objects.all()
    caja_abierta = Caja.objects.filter(abierta=True).first()

    if not caja_abierta:
        messages.error(request, "No hay ninguna caja abierta. Abre una caja antes de registrar ventas.")
        return redirect('abrir_caja')

    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente')
        tipo_comprobante = request.POST.get('tipo_comprobante')
        producto_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        precios = request.POST.getlist('precio[]')

        if not cliente_nombre or not producto_ids:
            messages.error(request, "Debes ingresar el cliente y al menos un producto.")
            return redirect('ventas_nueva')

        cliente_obj, _ = Cliente.objects.get_or_create(nombre=cliente_nombre)
        venta = Sale.objects.create(cliente=cliente_obj, tipo_comprobante=tipo_comprobante, total=Decimal("0.00"))

        total_venta = Decimal("0.00")

        for pid, cant, prec in zip(producto_ids, cantidades, precios):
            if not cant or not prec:
                continue
            try:
                cantidad = Decimal(cant)
                precio = Decimal(prec)
            except:
                continue

            producto = get_object_or_404(Producto, id=pid)

            if producto.stock < cantidad:
                messages.error(request, f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                venta.delete()  # eliminar venta incompleta
                return redirect('ventas_nueva')

            subtotal = cantidad * precio
            total_venta += subtotal

            SaleItem.objects.create(sale=venta, producto=producto, cantidad=cantidad, precio=precio)
            producto.stock -= cantidad
            producto.save()

        venta.total = total_venta
        venta.save()

        messages.success(request, f"Venta registrada correctamente. Total: S/. {total_venta:.2f}")

        if tipo_comprobante in ['Boleta', 'Factura']:
            return redirect('smartclick_redirect', sale_id=venta.id)
        else:
            return redirect('nota_venta', sale_id=venta.id)

    return render(request, 'inventario/registrar_venta.html', {'productos': productos})


def smartclick_redirect(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return redirect('/ventas/')  # Ajusta según tu flujo


def nota_venta(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = SaleItem.objects.filter(sale=sale)

    items_con_subtotal = []
    total = Decimal("0.00")
    for item in items:
        subtotal = item.cantidad * item.precio
        items_con_subtotal.append({
            'producto': item.producto,
            'cantidad': item.cantidad,
            'precio': item.precio,
            'subtotal': subtotal,
        })
        total += subtotal

    context = {
        'sale': sale,
        'items': items_con_subtotal,
        'total': total,
    }
    return render(request, 'ventas/nota_venta.html', context)
