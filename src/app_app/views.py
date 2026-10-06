from django.shortcuts import render

# Create your views here.
def suma_view(request):
    resultado = None
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            resultado = num1 + num2
        except ValueError:
            resultado = "Error: Ingresa números válidos"
            
    return render(request, 'app_app/suma.html', {'resultado': resultado})