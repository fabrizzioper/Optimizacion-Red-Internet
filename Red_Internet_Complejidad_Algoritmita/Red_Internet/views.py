# Red_Internet/views.py
from django.shortcuts import render
from django.conf import settings

def mapa_distritos(request):
    context = {
        'static_url': settings.STATIC_URL,  # Pasa la URL base de archivos estáticos al template
    }
    return render(request, 'mapa_distritos.html', context)
