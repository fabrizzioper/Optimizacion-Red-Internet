from django.db import models

class Distrito(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Nodo(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='nodos')
    nodo_id = models.CharField(max_length=100)  # ID del nodo (correspondiente a "id" en el JSON)
    y = models.FloatField()  # Coordenada Y (latitud)
    x = models.FloatField()  # Coordenada X (longitud)
    street_count = models.IntegerField()  # Número de calles conectadas al nodo
    highway = models.CharField(max_length=100, null=True, blank=True)
    ref = models.CharField(max_length=100, null=True, blank=True)
    geometry = models.JSONField()  # Coordenadas del nodo como JSON

    def __str__(self):
        return f"Nodo {self.nodo_id} en {self.distrito}"

class Conexion(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='conexiones')
    conexion_id = models.CharField(max_length=100)  # ID de la conexión (correspondiente a "id" en el JSON)
    osmid = models.JSONField()  # Acepta lista o valor único directamente
    id_inicio = models.CharField(max_length=100)  # ID de nodo inicial
    id_fin = models.CharField(max_length=100)  # ID de nodo final
    oneway = models.JSONField()  # Se guarda tal cual, lista o valor único
    lanes = models.CharField(max_length=10, null=True, blank=True)  # Número de carriles
    ref = models.CharField(max_length=100, null=True, blank=True)  # Referencia
    name = models.CharField(max_length=100, null=True, blank=True)  # Nombre de la conexión o calle
    highway = models.CharField(max_length=100)  # Tipo de carretera
    maxspeed = models.CharField(max_length=10, null=True, blank=True)  # Velocidad máxima permitida
    reversed = models.JSONField()  # Se guarda tal cual, lista o valor único
    length = models.FloatField()  # Longitud de la conexión
    junction = models.CharField(max_length=100, null=True, blank=True)  # Tipo de unión (por ejemplo, "roundabout")
    bridge = models.CharField(max_length=100, null=True, blank=True)  # Indica si es un puente
    access = models.CharField(max_length=100, null=True, blank=True)  # Tipo de acceso
    geometry = models.JSONField()  # Coordenadas como JSON en el campo de geometría

    def __str__(self):
        return f"Conexión {self.conexion_id} en {self.distrito}"
