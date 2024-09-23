# red/admin.py
from django.contrib import admin
from .models import Nodo, Conexion

admin.site.register(Nodo)
admin.site.register(Conexion)
