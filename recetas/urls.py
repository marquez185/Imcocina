from django.urls import path
from recetas import views

app_name = 'recetas'

urlpatterns = [
    path('agregarRecetas/', views.agregarRecetas, name="AgregarRecetas"),
    path('editarRecetas/', views.editarRecetas, name="EditarRecetas"),
    path('buscarRecetas/', views.buscarRecetas, name="BuscarRecetas"),
    path('guardarRecetas/', views.guardarRecetas, name="GuardarRecetas"),
    path('filtrarRecetas/', views.filtrarRecetas, name="FiltrarRecetas"),
    path('verNutricional/', views.verNutricional, name="VerNutricional"),
]