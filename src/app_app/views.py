# src/app_app/views.py
import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def suma_view(request):
    resultado = None
    archivo_info = None

    if request.method == 'POST':
        # 1. Procesar la suma
        if 'num1' in request.POST and 'num2' in request.POST:
            try:
                num1 = float(request.POST.get('num1', 0))
                num2 = float(request.POST.get('num2', 0))
                resultado = num1 + num2
            except ValueError:
                resultado = "Error: Ingresa números válidos"

        # 2. Procesar y guardar el archivo
        if 'archivo_subido' in request.FILES:
            archivo = request.FILES['archivo_subido']
            
            # Crear la carpeta media/ si no existe físicamente
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Guardar el archivo en el disco
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(archivo.name, archivo)

            archivo_info = {
                'nombre': filename,
                'tamano': round(archivo.size / 1024, 2),
                'tipo': archivo.content_type,
                'url': f"{settings.MEDIA_URL}{filename}"
            }

    return render(request, 'app_app/suma.html', {
        'resultado': resultado,
        'archivo_info': archivo_info
    })