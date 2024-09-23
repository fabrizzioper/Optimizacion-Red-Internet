# red/models.py
from django.db import models

class Nodo(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre

class Conexion(models.Model):
    origen = models.ForeignKey(Nodo, related_name='conexiones_origen', on_delete=models.CASCADE)
    destino = models.ForeignKey(Nodo, related_name='conexiones_destino', on_delete=models.CASCADE)
    peso = models.FloatField(default=1.0)  # Peso para definir el costo de la conexión

    def __str__(self):
        return f'{self.origen} -> {self.destino} ({self.peso})'
