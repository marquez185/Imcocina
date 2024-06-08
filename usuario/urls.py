from django.urls import path
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('login/', views.login, name="Login"),
    path('registro/', views.registro, name="Registro"),
    path('verificacion/', views.verificacion, name="Verificacion"),
    path('password/', views.password, name="Password"),
    path('tokenPassword/', views.tokenPassword, name="TokenPassword"),
    path('perfil/', views.perfil, name="Perfil"),
    path('updatePerfil/', views.updatePerfil, name="UpdatePerfil"),
]
