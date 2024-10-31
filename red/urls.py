from django.urls import path
from . import views

urlpatterns = [
    path('', views.agregar_nodo, name='agregar_nodo'),
    path('guardar_nodo/', views.guardar_nodo, name='guardar_nodo'),
    path('guardar_ruta/', views.guardar_ruta, name='guardar_ruta'),
    path('pruebas/', views.pruebas_view, name='pruebas')
]
