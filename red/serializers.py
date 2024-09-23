# red/serializers.py
from rest_framework import serializers
from .models import Nodo, Conexion

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['id', 'nombre', 'latitud', 'longitud']

class ConexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conexion
        fields = ['id', 'origen', 'destino', 'peso']
