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

def cargar_grafo_miraflores(request):
    # Ruta completa a los archivos de nodos y conexiones
    data_path = r"C:\Users\fabri\OneDrive\Escritorio\Optimizacion-Red-Internet\Red_Internet_Complejidad_Algoritmita\Red_Internet\static\Datos_Lima"

    # Imprimir archivos en el directorio para verificar
    print("Archivos en Datos_Lima:", os.listdir(data_path))

    # Archivos específicos para Miraflores
    nodo_file = os.path.join(data_path, "Miraflores_nodos.json")
    conexion_file = os.path.join(data_path, "Miraflores_conexiones.json")

    # Comprobar si los archivos existen antes de cargarlos
    if not os.path.exists(nodo_file) or not os.path.exists(conexion_file):
        return render(request, 'grafo_distritos.html', {
            'nodos_data': json.dumps([]),
            'conexiones_data': json.dumps([]),
            'error_message': "Archivos de datos no encontrados."
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
    }
    return render(request, 'grafo_distritos.html', context)