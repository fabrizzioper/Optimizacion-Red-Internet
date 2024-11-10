import json
import os
from django.core.management.base import BaseCommand
from Red_Internet.models import Distrito, Conexion, Nodo

class Command(BaseCommand):
    help = 'Carga datos de nodos y conexiones desde archivos JSON'

    def handle(self, *args, **options):
        datos_dir = os.path.join('Red_Internet', 'static', 'Datos_Lima')
        
        # Iterar sobre archivos JSON
        for archivo in os.listdir(datos_dir):
            distrito_nombre = archivo.split('_')[0]
            distrito, _ = Distrito.objects.get_or_create(nombre=distrito_nombre)
            
            # Verificar si ya hay conexiones o nodos cargados para el distrito
            if 'conexiones' in archivo:
                if not Conexion.objects.filter(distrito=distrito).exists():
                    self.cargar_conexiones(distrito, os.path.join(datos_dir, archivo))
                else:
                    print(f"Conexiones ya cargadas para {distrito.nombre}, omitiendo...")
            elif 'nodos' in archivo:
                if not Nodo.objects.filter(distrito=distrito).exists():
                    self.cargar_nodos(distrito, os.path.join(datos_dir, archivo))
                else:
                    print(f"Nodos ya cargados para {distrito.nombre}, omitiendo...")

    def cargar_conexiones(self, distrito, archivo_path):
        with open(archivo_path, 'r') as archivo:
            datos = json.load(archivo)
            for feature in datos['features']:
                props = feature['properties']
                Conexion.objects.create(
                    distrito=distrito,
                    conexion_id=feature['id'],
                    osmid=props.get('osmid'),
                    id_inicio=feature['id'].split(", ")[0].strip("("),
                    id_fin=feature['id'].split(", ")[1],
                    oneway=props.get('oneway'),
                    lanes=props.get('lanes'),
                    ref=props.get('ref'),
                    name=props.get('name'),
                    highway=props.get('highway'),
                    maxspeed=props.get('maxspeed'),
                    reversed=props.get('reversed'),
                    length=props.get('length'),
                    junction=props.get('junction'),
                    bridge=props.get('bridge'),
                    access=props.get('access'),
                    geometry=feature['geometry']['coordinates']
                )
            print(f"Conexiones cargadas para {distrito.nombre}")

    def cargar_nodos(self, distrito, archivo_path):
        with open(archivo_path, 'r') as archivo:
            datos = json.load(archivo)
            for feature in datos['features']:
                props = feature['properties']
                Nodo.objects.create(
                    distrito=distrito,
                    nodo_id=feature['id'],
                    y=props.get('y'),
                    x=props.get('x'),
                    street_count=props.get('street_count'),
                    highway=props.get('highway'),
                    ref=props.get('ref'),
                    geometry=feature['geometry']['coordinates']
                )
            print(f"Nodos cargados para {distrito.nombre}")
