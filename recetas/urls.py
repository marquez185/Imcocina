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
    path('toggle_favorito/', views.toggle_favorito, name="ToggleFavorito"),
    # Rutas CRUD para superusuarios
    path('crud_recetas/', views.crud_recetas, name="crud_recetas"),
    path('crear_receta/', views.crear_receta, name="crear_receta"),
    path('editar_receta/<int:receta_id>/', views.editar_receta, name="editar_receta"),
    path('eliminar_receta/<int:receta_id>/', views.eliminar_receta, name="eliminar_receta"),
    # Ruta para ver recetas de nuestra BD
    path('recetasAvaladas/', views.ver_recetas_avaladas, name="RecetasAvaladas"),
]
