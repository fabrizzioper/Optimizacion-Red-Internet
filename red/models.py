# red/models.py
from django.db import models

class Nodo(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre
