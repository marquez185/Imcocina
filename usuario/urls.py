from django.urls import path
from usuario import views

urlpatterns = [
    path('login/', views.login, name="Login"),
    path('registro/', views.registro, name="Registro"),
    path('password/', views.password, name="Password"),
    path('tokenPassword/', views.tokenPassword, name="TokenPassword"),
    path('updatePerfil', views.updatePerfil, name="UpdatePerfil"),
]
