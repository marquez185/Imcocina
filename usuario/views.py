from django.shortcuts import render, HttpResponse

def login(request):
    return HttpResponse("Login")

def registro(request):
    return HttpResponse("Registro")

def password(request):
    return HttpResponse("Password")

def tokenPassword(request):
    return HttpResponse("TokenPassword")

def updatePerfil(request):
    return HttpResponse("UpdatePerfil")

