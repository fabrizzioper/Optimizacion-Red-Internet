from django.db import models

class Nodo(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre

class Ruta(models.Model):
    nodo_inicial = models.ForeignKey(Nodo, related_name='rutas_iniciales', on_delete=models.CASCADE)
    nodo_final = models.ForeignKey(Nodo, related_name='rutas_finales', on_delete=models.CASCADE)
    peso = models.FloatField()
    geometria = models.JSONField()  # Almacena la geometría en formato GeoJSON

    def __str__(self):
        return f"Ruta de {self.nodo_inicial} a {self.nodo_final}"
