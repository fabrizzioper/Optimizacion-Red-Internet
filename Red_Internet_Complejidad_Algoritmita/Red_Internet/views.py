# views.py

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json
import os
import heapq  # Importamos heapq para el heap de prioridad

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

def dijkstra(adjacency_list, start, end):
    """
    Implementación del algoritmo de Dijkstra.
    
    :param adjacency_list: Diccionario que representa el grafo.
                           Cada clave es un nodo y su valor es una lista de tuplas (vecino, peso).
    :param start: Nodo de inicio.
    :param end: Nodo final.
    :return: Tupla (ruta, distancia) si existe ruta, de lo contrario, (None, None).
    """
    # Cola de prioridad: (distancia acumulada, nodo)
    heap = [(0, start)]
    # Distancias: nodo -> distancia mínima encontrada hasta ahora
    distances = {start: 0}
    # Predecesores: nodo -> nodo anterior en la ruta más corta
    predecessors = {}
    # Conjunto de nodos visitados
    visited = set()

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_node == end:
            # Reconstruir la ruta
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors.get(current_node)
            path.reverse()
            return path, current_distance

        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in adjacency_list.get(current_node, []):
            if neighbor in visited:
                continue
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))

    # Si llegamos aquí, no hay ruta
    return None, None

def calcular_ruta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos en 'calcular_ruta':", data)
        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            return JsonResponse({'error': 'Datos JSON inválidos.'}, status=400)

        nodo_inicio = data.get('nodo_inicio')
        nodo_final = data.get('nodo_final')
        distrito = data.get('distrito')

        print(f"nodo_inicio: {nodo_inicio}, nodo_final: {nodo_final}, distrito: {distrito}")

        if not all([nodo_inicio, nodo_final, distrito]):
            print("Faltan datos de entrada.")
            return JsonResponse({'error': 'Faltan datos de entrada.'}, status=400)

        # Ruta a los archivos de nodos y conexiones
        data_path = r"C:\Users\fabri\OneDrive\Escritorio\Optimizacion-Red-Internet\Red_Internet_Complejidad_Algoritmita\Red_Internet\static\Datos_Lima"
        nodo_file = os.path.join(data_path, f"{distrito}_nodos.json")
        conexion_file = os.path.join(data_path, f"{distrito}_conexiones.json")

        # Comprobar si los archivos existen
        if not os.path.exists(nodo_file) or not os.path.exists(conexion_file):
            print(f"Archivos no encontrados para el distrito {distrito}.")
            return JsonResponse({'error': 'Archivos de datos no encontrados para el distrito especificado.'}, status=404)

        # Cargar datos
        try:
            with open(nodo_file, 'r') as f:
                nodos_geojson = json.load(f)
            nodos = nodos_geojson.get('features', [])
            print(f"Se cargaron {len(nodos)} nodos.")
        except Exception as e:
            print(f"Error al cargar nodos: {e}")
            return JsonResponse({'error': 'Error al cargar nodos.'}, status=500)

        try:
            with open(conexion_file, 'r') as f:
                conexiones_geojson = json.load(f)
            conexiones = conexiones_geojson.get('features', [])
            print(f"Se cargaron {len(conexiones)} conexiones.")
        except Exception as e:
            print(f"Error al cargar conexiones: {e}")
            return JsonResponse({'error': 'Error al cargar conexiones.'}, status=500)

        # Crear el grafo como lista de adyacencia
        adjacency_list = {}

        # Agregar nodos al grafo
        for nodo in nodos:
            try:
                nodo_id = str(nodo['id'])
                # Extraer lat y lng desde geometry.coordinates [lng, lat]
                lng, lat = nodo['geometry']['coordinates']
                adjacency_list.setdefault(nodo_id, [])  # Inicializar lista de vecinos
                print(f"Agregado nodo: {nodo_id} con lat={lat}, lng={lng}")
            except KeyError as e:
                print(f"Falta clave en nodo: {e}")
            except Exception as e:
                print(f"Error al procesar nodo: {e}")

        # Agregar aristas al grafo
        for conexion in conexiones:
            try:
                conexion_id = conexion['id']
                # Supongo que el formato de 'id' es "(source, target, 0)"
                # Necesitamos extraer 'source' y 'target'
                # Remover paréntesis y dividir por coma
                source_target = conexion_id.strip('()').split(',')
                if len(source_target) >= 2:
                    source = source_target[0].strip()
                    target = source_target[1].strip()
                    peso = conexion['properties'].get('length', 1)  # Usar 'length' como peso
                    # Asegurarse de que source y target existan en nodos
                    if source in adjacency_list and target in adjacency_list:
                        # Agregar arista bidireccional
                        adjacency_list[source].append((target, peso))
                        adjacency_list[target].append((source, peso))
                        print(f"Agregada arista: {source} - {target} con peso {peso}")
                    else:
                        print(f"Fuente o destino no existe en nodos: {source}, {target}")
                else:
                    print(f"Formato de 'id' de conexión inválido: {conexion_id}")
            except KeyError as e:
                print(f"Falta clave en conexión: {e}")
            except Exception as e:
                print(f"Error al procesar conexión: {e}")

        print(f"Grafo creado con {len(adjacency_list)} nodos.")

        # Verificar que los nodos existen en el grafo
        if nodo_inicio not in adjacency_list or nodo_final not in adjacency_list:
            print("Uno o ambos nodos no existen en el grafo.")
            return JsonResponse({'error': 'Uno o ambos nodos no existen en el grafo.'}, status=400)

        # Calcular la ruta más corta usando Dijkstra
        ruta, distancia = dijkstra(adjacency_list, nodo_inicio, nodo_final)

        if ruta is None:
            print("No existe una ruta entre los nodos especificados.")
            return JsonResponse({'error': 'No existe una ruta entre los nodos especificados.'}, status=400)

        print(f"Ruta encontrada: {ruta} con distancia {distancia}")

        # Obtener las coordenadas de los nodos en la ruta para visualización
        coordenadas = []
        # Crear un diccionario para acceder rápidamente a las coordenadas de cada nodo
        nodo_coords = {}
        for nodo in nodos:
            nodo_id = str(nodo['id'])
            try:
                lng, lat = nodo['geometry']['coordinates']
                nodo_coords[nodo_id] = (lat, lng)
            except KeyError as e:
                print(f"Falta clave en nodo para coordenadas: {e}")
            except Exception as e:
                print(f"Error al obtener coordenadas del nodo: {e}")

        for nodo_id in ruta:
            coords = nodo_coords.get(nodo_id)
            if coords:
                coordenadas.append([coords[0], coords[1]])  # [lat, lng]
            else:
                print(f"Coordenadas no encontradas para el nodo: {nodo_id}")
                coordenadas.append([0, 0])  # Valor por defecto o manejo alternativo

        print(f"Coordenadas de la ruta: {coordenadas}")

        return JsonResponse({
            'ruta': ruta,
            'distancia': distancia,
            'coordenadas': coordenadas
        })
    else:
        print("Método HTTP no permitido para 'calcular_ruta'.")
        return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)
