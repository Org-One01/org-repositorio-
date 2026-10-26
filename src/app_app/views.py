# src/app_app/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Prefetch
from django.db.models.fields.related import ForeignKey

from .models import (
    ProductoRopa, Proveedor, Etiqueta, Coleccion,
    DetalleProducto, Variante, Resena,
)


# ─────────────────────────────────────────────────────────────
# HELPERS M:N SEGUROS PARA MULTI-BD
# ─────────────────────────────────────────────────────────────
def _through_fields(instance, field_name):
    """Devuelve (source_fk, target_fk) de la tabla intermedia."""
    field = instance._meta.get_field(field_name)
    through = field.remote_field.through
    source_fk = target_fk = None
    for f in through._meta.fields:
        if isinstance(f, ForeignKey):
            if f.remote_field.model is type(instance):
                source_fk = f
            elif f.remote_field.model is field.remote_field.model:
                target_fk = f
    return through, source_fk, target_fk


def sync_m2m(instance, field_name, related_ids, db_alias):
    """
    Sincroniza una relación M:N escribiendo directamente en la tabla
    intermedia con `.using(db_alias)`. Evita el router por defecto.
    """
    through, source_fk, target_fk = _through_fields(instance, field_name)
    if not source_fk or not target_fk:
        return

    # Limpia los vínculos actuales
    through.objects.using(db_alias).filter(
        **{f"{source_fk.name}_id": instance.pk}
    ).delete()

    # Inserta los nuevos vínculos
    ids = [int(x) for x in related_ids if str(x).strip()]
    if ids:
        through.objects.using(db_alias).bulk_create([
            through(**{
                f"{source_fk.name}_id": instance.pk,
                f"{target_fk.name}_id": rid,
            })
            for rid in ids
        ])


def get_m2m_ids(instance, field_name, db_alias):
    """Devuelve los IDs actualmente vinculados (M:N) desde la BD indicada."""
    through, source_fk, target_fk = _through_fields(instance, field_name)
    if not source_fk or not target_fk:
        return set()
    return set(
        through.objects.using(db_alias)
        .filter(**{f"{source_fk.name}_id": instance.pk})
        .values_list(f"{target_fk.name}_id", flat=True)
    )


# ─────────────────────────────────────────────────────────────
# VISTA PRINCIPAL
# ─────────────────────────────────────────────────────────────
def suma_view(request):
    resultado = None
    archivo_info = None

    db_seleccionada = request.GET.get('db', request.POST.get('db_activa', 'default'))
    if db_seleccionada not in settings.DATABASES:
        db_seleccionada = 'default'

    engine_name = settings.DATABASE_LABELS[db_seleccionada]
    database_options = [
        {'alias': alias, 'label': label}
        for alias, label in settings.DATABASE_LABELS.items()
    ]

    if request.method == 'POST':
        # ── 1. Guardar prenda (con 1:1, 1:N y N:N) ──
        if 'guardar_ropa' in request.POST:
            db_activa = request.POST.get('db_activa', db_seleccionada)
            if db_activa not in settings.DATABASES:
                db_activa = 'default'

            proveedor_id = request.POST.get('proveedor_id') or None

            nuevo_producto = ProductoRopa.objects.using(db_activa).create(
                nombre    = request.POST.get('nombre_ropa'),
                categoria = request.POST.get('categoria_ropa'),
                talla     = request.POST.get('talla_ropa'),
                precio    = request.POST.get('precio_ropa'),
                proveedor_id = proveedor_id,   # 1:N
            )

            # 1:1 — Detalle
            DetalleProducto.objects.using(db_activa).create(
                producto_id            = nuevo_producto.id,
                descripcion            = request.POST.get('descripcion', ''),
                material               = request.POST.get('material', ''),
                pais_fabricacion       = request.POST.get('pais_fabricacion', ''),
                instrucciones_cuidado  = request.POST.get('instrucciones_cuidado', ''),
            )

            # N:N — Etiquetas y Colecciones
            sync_m2m(nuevo_producto, 'etiquetas',
                     request.POST.getlist('etiquetas_ids'), db_activa)
            sync_m2m(nuevo_producto, 'colecciones',
                     request.POST.getlist('colecciones_ids'), db_activa)

            return redirect(f"/?db={db_activa}")

        # ── 2. Suma ──
        if 'num1' in request.POST and 'num2' in request.POST:
            try:
                num1 = float(request.POST.get('num1', 0))
                num2 = float(request.POST.get('num2', 0))
                resultado = num1 + num2
            except ValueError:
                resultado = "Error: Ingresa números válidos"

        # ── 3. Subida de archivos ──
        if 'archivo_subido' in request.FILES:
            archivo = request.FILES['archivo_subido']
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(archivo.name, archivo)
            archivo_info = {
                'nombre': filename,
                'tamano': round(archivo.size / 1024, 2),
                'tipo'  : archivo.content_type,
                'url'   : f"{settings.MEDIA_URL}{filename}",
            }

       # ── AUTO-CREACIÓN DE DATOS POR DEFECTO (Si las tablas están vacías) ──
    if not Proveedor.objects.using(db_seleccionada).exists():
        Proveedor.objects.using(db_seleccionada).bulk_create([
            Proveedor(nombre='Proveedor Textil S.A.', contacto='Juan', pais='Colombia'),
            Proveedor(nombre='Importaciones XYZ', contacto='Maria', pais='China'),
            Proveedor(nombre='Moda Local', contacto='Carlos', pais='México'),
        ])
    
    if not Etiqueta.objects.using(db_seleccionada).exists():
        Etiqueta.objects.using(db_seleccionada).bulk_create([
            Etiqueta(nombre='Nuevo'), 
            Etiqueta(nombre='Oferta'), 
            Etiqueta(nombre='Premium'),
            Etiqueta(nombre='Ecológico')
        ])
    
    if not Coleccion.objects.using(db_seleccionada).exists():
        Coleccion.objects.using(db_seleccionada).bulk_create([
            Coleccion(nombre='Verano 2024', temporada='Verano'),
            Coleccion(nombre='Invierno 2024', temporada='Invierno'),
            Coleccion(nombre='Básicos', temporada='Todo el año'),
        ])

    # ── Listas para los <select> del formulario ──
    proveedores = Proveedor.objects.using(db_seleccionada).all()
    etiquetas   = Etiqueta.objects.using(db_seleccionada).all()
    colecciones = Coleccion.objects.using(db_seleccionada).all()

    # ── Productos con relaciones precargadas (todo en la BD activa) ──
    productos_ropa = (
        ProductoRopa.objects
        .using(db_seleccionada)
        .select_related('proveedor')
        .prefetch_related(
            Prefetch('detalle',
                     queryset=DetalleProducto.objects.using(db_seleccionada)),
            Prefetch('etiquetas',
                     queryset=Etiqueta.objects.using(db_seleccionada)),
            Prefetch('colecciones',
                     queryset=Coleccion.objects.using(db_seleccionada)),
            Prefetch('variantes',
                     queryset=Variante.objects.using(db_seleccionada)),
            Prefetch('resenas',
                     queryset=Resena.objects.using(db_seleccionada)),
        )
        .order_by('-fecha_creacion')
    )

    return render(request, 'app_app/suma.html', {
        'resultado'          : resultado,
        'archivo_info'       : archivo_info,
        'productos_ropa'     : productos_ropa,
        'proveedores'        : proveedores,
        'etiquetas'          : etiquetas,
        'colecciones'        : colecciones,
        'db_seleccionada'    : db_seleccionada,
        'engine_name'        : engine_name,
        'database_options'   : database_options,
    })


# ─────────────────────────────────────────────────────────────
# EDITAR
# ─────────────────────────────────────────────────────────────
def editar_producto(request, pk, db_engine='default'):
    if db_engine not in settings.DATABASES:
        db_engine = 'default'

    producto = get_object_or_404(ProductoRopa.objects.using(db_engine), pk=pk)

    if request.method == 'POST':
        # ── Datos básicos + 1:N ──
        producto.nombre       = request.POST.get('nombre')
        producto.categoria    = request.POST.get('categoria')
        producto.talla        = request.POST.get('talla')
        producto.precio       = request.POST.get('precio')
        producto.proveedor_id = request.POST.get('proveedor_id') or None
        producto.save(using=db_engine)

        # ── 1:1 Detalle (crear si no existe, actualizar si existe) ──
        detalle, creado = DetalleProducto.objects.using(db_engine).get_or_create(
            producto_id=producto.id,
            defaults={
                'descripcion'           : request.POST.get('descripcion', ''),
                'material'              : request.POST.get('material', ''),
                'pais_fabricacion'      : request.POST.get('pais_fabricacion', ''),
                'instrucciones_cuidado' : request.POST.get('instrucciones_cuidado', ''),
            },
        )
        if not creado:
            detalle.descripcion           = request.POST.get('descripcion', '')
            detalle.material              = request.POST.get('material', '')
            detalle.pais_fabricacion      = request.POST.get('pais_fabricacion', '')
            detalle.instrucciones_cuidado = request.POST.get('instrucciones_cuidado', '')
            detalle.save(using=db_engine)

        # ── N:N ──
        sync_m2m(producto, 'etiquetas',
                 request.POST.getlist('etiquetas_ids'), db_engine)
        sync_m2m(producto, 'colecciones',
                 request.POST.getlist('colecciones_ids'), db_engine)

        return redirect(f'/?db={db_engine}')

    # ── Datos para el template ──
    detalle           = DetalleProducto.objects.using(db_engine).filter(producto_id=pk).first()
    proveedores       = Proveedor.objects.using(db_engine).all()
    etiquetas         = Etiqueta.objects.using(db_engine).all()
    colecciones       = Coleccion.objects.using(db_engine).all()
    etiquetas_act     = get_m2m_ids(producto, 'etiquetas', db_engine)
    colecciones_act   = get_m2m_ids(producto, 'colecciones', db_engine)

    return render(request, 'app_app/editar_producto.html', {
        'producto'               : producto,
        'detalle'                : detalle,
        'db_engine'              : db_engine,
        'proveedores'            : proveedores,
        'etiquetas'              : etiquetas,
        'colecciones'            : colecciones,
        'etiquetas_act'          : etiquetas_act,
        'colecciones_act'        : colecciones_act,
    })


# ─────────────────────────────────────────────────────────────
# ELIMINAR
# ─────────────────────────────────────────────────────────────
def eliminar_producto(request, pk, db_engine='default'):
    if db_engine not in settings.DATABASES:
        db_engine = 'default'

    producto = get_object_or_404(ProductoRopa.objects.using(db_engine), pk=pk)

    if request.method == 'POST':
        # Cascada explícita (todo en la BD activa)
        DetalleProducto.objects.using(db_engine).filter(producto_id=pk).delete()
        Variante.objects.using(db_engine).filter(producto_id=pk).delete()
        Resena.objects.using(db_engine).filter(producto_id=pk).delete()

        # Vínculos M:N (solo la tabla intermedia)
        sync_m2m(producto, 'etiquetas',   [], db_engine)
        sync_m2m(producto, 'colecciones', [], db_engine)

        ProductoRopa.objects.using(db_engine).filter(pk=pk).delete()
        return redirect(f'/?db={db_engine}')

    # Info de cascada para el template
    tiene_detalle   = DetalleProducto.objects.using(db_engine).filter(producto_id=pk).exists()
    variantes_count = Variante.objects.using(db_engine).filter(producto_id=pk).count()
    resenas_count   = Resena.objects.using(db_engine).filter(producto_id=pk).count()

    return render(request, 'app_app/confirmar_eliminar.html', {
        'producto'        : producto,
        'db_engine'       : db_engine,
        'tiene_detalle'   : tiene_detalle,
        'variantes_count' : variantes_count,
        'resenas_count'   : resenas_count,
    })