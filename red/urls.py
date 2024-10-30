from django.urls import path
from . import views

urlpatterns = [
    path('', views.agregar_nodo, name='agregar_nodo'),
    path('guardar_nodo/', views.guardar_nodo, name='guardar_nodo'),
]
