from django.shortcuts import render
from django.http import JsonResponse
import folium
import requests
from .models import Nodo, Ruta

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
            popup=f"ID: {nodo.id} - Nombre: {nodo.nombre}"
        ).add_to(mapa_principal)

    # Recuperar las rutas almacenadas en la base de datos y añadirlas al mapa
    rutas = Ruta.objects.all()
    for ruta in rutas:
        # Dibujar la ruta utilizando la geometría almacenada
        folium.GeoJson(
            ruta.geometria,
            name=f"Ruta ID: {ruta.id} - Peso: {ruta.peso}"
        ).add_to(mapa_principal)

    # Convertimos el mapa a HTML
    mapa_principal_html = mapa_principal._repr_html_()
    
    # Pasamos el mapa principal al contexto de la plantilla
    return render(request, 'agregar_nodo.html', {
        'mapa_principal': mapa_principal_html
    })

def obtener_ruta_osrm(lat_inicio, lon_inicio, lat_fin, lon_fin):
    """Obtiene la ruta más corta que sigue las calles usando OSRM."""
    url = f"http://router.project-osrm.org/route/v1/driving/{lon_inicio},{lat_inicio};{lon_fin},{lat_fin}"
    response = requests.get(url, params={'overview': 'full', 'geometries': 'geojson'})
    ruta = response.json()
    if ruta['code'] == 'Ok':
        return ruta['routes'][0]['geometry']  # Devolver la geometría de la ruta
    return None

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

def guardar_ruta(request):
    if request.method == "POST":
        nodo_inicial_id = request.POST.get('nodoInicial')
        nodo_final_id = request.POST.get('nodoFinal')
        peso = request.POST.get('peso')

        try:
            nodo_inicial = Nodo.objects.get(id=nodo_inicial_id)
            nodo_final = Nodo.objects.get(id=nodo_final_id)

            # Obtener la ruta entre los nodos usando OSRM
            ruta_geojson = obtener_ruta_osrm(nodo_inicial.latitud, nodo_inicial.longitud, nodo_final.latitud, nodo_final.longitud)
            
            if ruta_geojson:
                # Guardar la ruta en la base de datos, incluyendo la geometría
                Ruta.objects.create(
                    nodo_inicial=nodo_inicial,
                    nodo_final=nodo_final,
                    peso=float(peso),
                    geometria=ruta_geojson
                )
                return JsonResponse({'status': 'Ruta guardada correctamente'})
            else:
                return JsonResponse({'status': 'Error al calcular la ruta. Verifique los puntos y su conexión.'}, status=400)
        except Nodo.DoesNotExist:
            return JsonResponse({'status': 'Error: Nodo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'Error al guardar la ruta', 'error': str(e)}, status=400)

    return JsonResponse({'status': 'Error: Solicitud inválida'}, status=400)

def pruebas_view(request):
    return render(request, 'pruebas.html')
