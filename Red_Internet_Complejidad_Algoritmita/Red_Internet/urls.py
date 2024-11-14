# # Red_Internet/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.mapa_distritos, name='mapa_distritos'),
# ]


# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_distritos, name='mapa_distritos'),
    path('grafo_miraflores/', views.cargar_grafo_miraflores, name='grafo_miraflores'),
]