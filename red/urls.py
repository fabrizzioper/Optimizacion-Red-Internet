# red/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import NodoViewSet, ConexionViewSet, visualizar_red, agregar_nodo, agregar_conexion

router = DefaultRouter()
router.register(r'nodos', NodoViewSet)
router.register(r'conexiones', ConexionViewSet)

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('visualizar_red/', views.visualizar_red, name='visualizar_red'),  # Ruta para la vista HTML
    path('api/', include(router.urls)),  # Rutas para la API de nodos y conexiones
    path('api/agregar_nodo/', views.agregar_nodo, name='agregar_nodo'),  # Ruta para agregar nodos
    path('api/agregar_conexion/', views.agregar_conexion, name='agregar_conexion'),  # Ruta para agregar conexiones
]
