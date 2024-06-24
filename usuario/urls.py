from django.urls import path
from django.contrib.auth.views import LogoutView
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('login/', views.login, name="Login"),
    path('registro/', views.registro, name="Registro"),
    path('verificacion/', views.verificacion, name="Verificacion"),
    path('password-reset/<uidb64>/<token>/', views.password, name="Password"),
    path('tokenPassword/', views.tokenPassword, name="TokenPassword"),
    path('perfil/', views.perfil, name="Perfil"),
    path('updatePerfil/', views.updatePerfil, name="UpdatePerfil"),
    path('logout/', LogoutView.as_view(), name="Logout"),
    path('favoritas/', views.recetas_favoritas, name="Favoritas"),
]
