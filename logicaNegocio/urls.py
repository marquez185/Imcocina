from django.urls import path
from logicaNegocio import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('noticias/', views.noticias, name="Noticias"),
    path('desperdicio/', views.desperdicio, name="ConsejosDesperdicio"),
    path('nosotros/', views.nosotros, name="Nosotros"),
    path('politicas-privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('terminos-uso/', views.terminos_uso, name='terminos_uso'),
]