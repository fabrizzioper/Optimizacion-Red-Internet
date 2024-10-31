# red/admin.py
from django.contrib import admin
from .models import Nodo, Ruta

admin.site.register(Nodo)
admin.site.register(Ruta)
