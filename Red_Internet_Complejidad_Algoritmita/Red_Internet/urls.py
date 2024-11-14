# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.mapa_distritos, name='mapa_distritos'),
#     path('grafo_<str:distrito>/', views.cargar_grafo_distrito, name='grafo_distrito'),
# ]




from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_distritos, name='mapa_distritos'),
    path('grafo_<str:distrito>/', views.cargar_grafo_distrito, name='grafo_distrito'),
    path('calcular_ruta/', views.calcular_ruta, name='calcular_ruta'),  # Nueva ruta
]
