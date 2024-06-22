from django.shortcuts import render, HttpResponse
from .API_recetas import buscar_recetas_ingredientes

# Create your views here.

def agregarRecetas(request):
    return HttpResponse("AgregarRecetas")

def editarRecetas(request):
    return HttpResponse("EditarRecetas")

def buscarRecetas(request):
    ingredientes = request.GET.get('ingredientes', '')
    recetas = buscar_recetas_ingredientes(ingredientes, num_recetas=10)
    context = {'recetas': recetas}
    return render(request, "recetas/buscarRecetas.html", context)

def guardarRecetas(request):
    return HttpResponse("GuardarRecetas")

def filtrarRecetas(request):
    return HttpResponse("FiltrarRecetas")

def verNutricional(request):
    return HttpResponse("VerNutricional")