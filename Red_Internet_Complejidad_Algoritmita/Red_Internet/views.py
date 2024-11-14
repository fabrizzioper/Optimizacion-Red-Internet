from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json
import os
import networkx as nx

def mapa_distritos(request):
    context = {
        'static_url': settings.STATIC_URL,
    }
    return render(request, 'mapa_distritos.html', context)

def cargar_grafo_distrito(request, distrito):
    # Ruta a los archivos de nodos y conexiones
    data_path = r"C:\Users\fabri\OneDrive\Escritorio\Optimizacion-Red-Internet\Red_Internet_Complejidad_Algoritmita\Red_Internet\static\Datos_Lima"

    # Archivos específicos para el distrito seleccionado
    nodo_file = os.path.join(data_path, f"{distrito}_nodos.json")
    conexion_file = os.path.join(data_path, f"{distrito}_conexiones.json")

    # Comprobar si los archivos existen antes de cargarlos
    if not os.path.exists(nodo_file) or not os.path.exists(conexion_file):
        return render(request, 'grafo_distritos.html', {
            'nodos_data': json.dumps([]),
            'conexiones_data': json.dumps([]),
            'error_message': f"Archivos de datos no encontrados para el distrito {distrito}."
        })

    # Cargar datos de nodos y conexiones
    with open(nodo_file, 'r') as f:
        nodos_data = json.load(f)

    with open(conexion_file, 'r') as f:
        conexiones_data = json.load(f)

    # Enviar datos a la plantilla
    context = {
        'nodos_data': json.dumps(nodos_data),
        'conexiones_data': json.dumps(conexiones_data),
        'distrito': distrito  # Pasar el nombre del distrito para usar en el HTML
    }
    return render(request, 'grafo_distritos.html', context)