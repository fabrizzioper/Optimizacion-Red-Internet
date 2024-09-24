# red/views.py

import json
from django.shortcuts import render
from rest_framework import viewsets
from .models import Nodo, Conexion
from .serializers import NodoSerializer, ConexionSerializer
import folium
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')  # Renderiza la plantilla de la página de inicio

# API views
class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer

class ConexionViewSet(viewsets.ModelViewSet):
    queryset = Conexion.objects.all()
    serializer_class = ConexionSerializer

# Función para obtener los nodos y generar el mapa
# Función para obtener los nodos y generar el mapa
def generar_mapa():
    # Crear un mapa centrado en Lima, Perú
    mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=13)

    # Obtener todos los nodos de la base de datos
    nodos = Nodo.objects.all()
    for nodo in nodos:
        folium.Marker(
            [nodo.latitud, nodo.longitud],
            # Mostramos el ID y el nombre en el popup
            popup=f'ID: {nodo.id}<br>Nombre: {nodo.nombre}',
            tooltip='Haz clic para seleccionar'
        ).add_to(mapa)
    
    # Obtener todas las conexiones y dibujar las líneas entre los nodos
    conexiones = Conexion.objects.all()
    for conexion in conexiones:
        origen = [conexion.origen.latitud, conexion.origen.longitud]
        destino = [conexion.destino.latitud, conexion.destino.longitud]
        folium.PolyLine(locations=[origen, destino], color="blue").add_to(mapa)

    # Retornar el HTML del mapa
    return mapa._repr_html_()


# HTML view para visualizar el mapa
def visualizar_red(request):
    mapa_html = generar_mapa()  # Generar el mapa con nodos y conexiones
    return render(request, 'visualizar_red.html', {'mapa': mapa_html})

@csrf_exempt  # Si tienes problemas con CSRF, puedes usar esta función para exentar la protección
def agregar_nodo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # Obtener datos del cuerpo de la solicitud
        nombre = data.get('nombre')  # Obtener el nombre del nodo
        latitud = data.get('latitud')  # Obtener la latitud del nodo
        longitud = data.get('longitud')  # Obtener la longitud del nodo

        # Verificar que los datos estén completos
        if not nombre or not latitud or not longitud:
            return JsonResponse({'error': 'Faltan datos'}, status=400)

        # Crear y guardar el nodo en la base de datos
        nodo = Nodo(nombre=nombre, latitud=latitud, longitud=longitud)
        nodo.save()

        return JsonResponse({'mensaje': 'Nodo agregado correctamente', 'nodo_id': nodo.id})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# API para agregar una conexión entre dos nodos
@csrf_exempt
def agregar_conexion(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        origen_id = data.get('origen')
        destino_id = data.get('destino')
        peso = data.get('peso')

        if not origen_id or not destino_id or peso is None:
            return JsonResponse({'error': 'Faltan datos'}, status=400)

        try:
            origen = Nodo.objects.get(id=origen_id)
            destino = Nodo.objects.get(id=destino_id)
            conexion = Conexion(origen=origen, destino=destino, peso=float(peso))
            conexion.save()

            return JsonResponse({'mensaje': 'Conexión agregada correctamente'})
        except Nodo.DoesNotExist:
            return JsonResponse({'error': 'Nodo no encontrado'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'El peso debe ser un número válido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)