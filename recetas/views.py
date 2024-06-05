from django.shortcuts import render, HttpResponse

# Create your views here.

def agregarRecetas(request):
    return HttpResponse("AgregarRecetas")

def editarRecetas(request):
    return HttpResponse("EditarRecetas")

def buscarRecetas(request):
    return render(request, "recetas/buscarRecetas.html")

def guardarRecetas(request):
    return HttpResponse("GuardarRecetas")

def filtrarRecetas(request):
    return HttpResponse("FiltrarRecetas")

def verNutricional(request):
    return HttpResponse("VerNutricional")