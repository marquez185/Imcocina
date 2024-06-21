from django.urls import path
from logicaNegocio import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('nosotros/', views.nosotros, name="Nosotros"),
]