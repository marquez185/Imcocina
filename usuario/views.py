from django.shortcuts import render, HttpResponse

def login(request):
    return render(request, "usuario/login.html")

def registro(request):
    return render(request, "usuario/registro.html")

def verificacion(request):
    return render(request, "usuario/verificacion.html")

def password(request):
    return render(request, "usuario/password.html")

def tokenPassword(request):
    return HttpResponse("TokenPassword")

def updatePerfil(request):
    return HttpResponse("UpdatePerfil")

