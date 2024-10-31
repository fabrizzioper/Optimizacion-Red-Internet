# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# import folium

# # Lista temporal para almacenar nodos (se recomienda usar una base de datos en producción)
# nodos = []

# def agregar_nodo(request):
#     # Crear el mapa principal centrado en Lima, Perú
#     mapa_principal = folium.Map(
#         location=[-12.0464, -77.0428],
#         zoom_start=13,
#         control_scale=True,
#         width='100%',
#         height='100%',
#     )

#     # Añadir los nodos almacenados al mapa principal
#     for nodo in nodos:
#         folium.Marker(
#             location=[nodo['latitud'], nodo['longitud']],
#             popup=f"Nombre: {nodo['nombre']}"
#         ).add_to(mapa_principal)

#     # Convertimos el mapa a HTML
#     mapa_principal_html = mapa_principal._repr_html_()
    
#     # Pasamos el mapa principal al contexto de la plantilla
#     return render(request, 'agregar_nodo.html', {
#         'mapa_principal': mapa_principal_html
#     })

# def guardar_nodo(request):
#     if request.method == "POST":
#         # Obtener los datos enviados desde el frontend
#         nombre = request.POST.get('nombre')
#         latitud = request.POST.get('latitud')
#         longitud = request.POST.get('longitud')

#         # Guardar el nodo en la lista (o en la base de datos)
#         nodos.append({
#             'nombre': nombre,
#             'latitud': float(latitud),
#             'longitud': float(longitud)
#         })

#         # Responder con éxito
#         return JsonResponse({'status': 'Nodo guardado correctamente'})
#     return JsonResponse({'status': 'Error'}, status=400)

# red/views.py
from django.shortcuts import render
from django.http import JsonResponse
import folium
from .models import Nodo  # Importa el modelo Nodo

def agregar_nodo(request):
    # Crear el mapa principal centrado en Lima, Perú
    mapa_principal = folium.Map(
        location=[-12.0464, -77.0428],
        zoom_start=13,
        control_scale=True,
        width='100%',
        height='100%'
    )

    # Recuperar los nodos almacenados en la base de datos y añadirlos al mapa
    nodos = Nodo.objects.all()
    for nodo in nodos:
        folium.Marker(
            location=[nodo.latitud, nodo.longitud],
            popup=f"Nombre: {nodo.nombre}"
        ).add_to(mapa_principal)

    # Convertimos el mapa a HTML
    mapa_principal_html = mapa_principal._repr_html_()
    
    # Pasamos el mapa principal al contexto de la plantilla
    return render(request, 'agregar_nodo.html', {
        'mapa_principal': mapa_principal_html
    })

def guardar_nodo(request):
    if request.method == "POST":
       
        nombre = request.POST.get('nombre')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

     
        Nodo.objects.create(
            nombre=nombre,
            latitud=float(latitud),
            longitud=float(longitud)
        )

        # Responder con éxito
        return JsonResponse({'status': 'Nodo guardado correctamente'})
    return JsonResponse({'status': 'Error'}, status=400)

def pruebas_view(request):
    return render(request, 'pruebas.html')
