# src/app_app/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import ProductoRopa

def suma_view(request):
    resultado = None
    archivo_info = None

    # 1. Determinar qué motor de base de datos seleccionó el usuario (por defecto 'default')
    db_seleccionada = request.GET.get('db', request.POST.get('db_activa', 'default'))
    if db_seleccionada not in settings.DATABASES:
        db_seleccionada = 'default'

    # Obtener el nombre legible del motor
    engine_name = settings.DATABASES[db_seleccionada]['ENGINE'].split('.')[-1].upper()

    if request.method == 'POST':
        # Guardar producto en la BD seleccionada
        if 'guardar_ropa' in request.POST:
            nombre = request.POST.get('nombre_ropa')
            categoria = request.POST.get('categoria_ropa')
            talla = request.POST.get('talla_ropa')
            precio = request.POST.get('precio_ropa')

            nuevo_producto = ProductoRopa(
                nombre=nombre,
                categoria=categoria,
                talla=talla,
                precio=precio
            )
            # Guarda explícitamente en la BD elegida
            nuevo_producto.save(using=db_seleccionada)
            return redirect(f"/?db={db_seleccionada}")

        # Operación de Suma
        if 'num1' in request.POST and 'num2' in request.POST:
            try:
                num1 = float(request.POST.get('num1', 0))
                num2 = float(request.POST.get('num2', 0))
                resultado = num1 + num2
            except ValueError:
                resultado = "Error: Ingresa números válidos"

        # Subida de Archivos
        if 'archivo_subido' in request.FILES:
            archivo = request.FILES['archivo_subido']
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(archivo.name, archivo)

            archivo_info = {
                'nombre': filename,
                'tamano': round(archivo.size / 1024, 2),
                'tipo': archivo.content_type,
                'url': f"{settings.MEDIA_URL}{filename}"
            }

    # Consultar prendas en la BD seleccionada
    try:
        productos_ropa = ProductoRopa.objects.using(db_seleccionada).all().order_by('-fecha_creacion')
    except Exception:
        productos_ropa = []

    return render(request, 'app_app/suma.html', {
        'resultado': resultado,
        'archivo_info': archivo_info,
        'productos_ropa': productos_ropa,
        'db_seleccionada': db_seleccionada,
        'engine_name': engine_name
    })
# src/app_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductoRopa

def editar_producto(request, pk, db_engine='default'):
    # Obtiene el producto de la base de datos activa
    producto = get_object_or_404(ProductoRopa.objects.using(db_engine), pk=pk)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.categoria = request.POST.get('categoria')
        producto.talla = request.POST.get('talla')
        producto.precio = request.POST.get('precio')
        
        # Guarda los cambios en la base de datos correspondiente
        producto.save(using=db_engine)
        
        # Redirige a la página principal con el parámetro de la base de datos activa
        return redirect(f'/?db={db_engine}')
        
    return render(request, 'app_app/editar_producto.html', {
        'producto': producto, 
        'db_engine': db_engine
    })

def eliminar_producto(request, pk, db_engine='default'):
    producto = get_object_or_404(ProductoRopa.objects.using(db_engine), pk=pk)
    
    if request.method == 'POST':
        producto.delete(using=db_engine)
        return redirect(f'/?db={db_engine}')

    return render(request, 'app_app/confirmar_eliminar.html', {
        'producto': producto, 
        'db_engine': db_engine
    })