from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from BD.models import Receta, Favoritos  # Importar desde la ubicación correcta
from recetas.API_recetas import buscar_recetas_ingredientes, obtener_recetas
import json

# Create your views here.
'''MANEJO DE NOMBRE DE SESION'''

def nombre_usuario(request):
    if request.user.is_authenticated:
        return request.user.first_name
    return None

def agregarRecetas(request):
    return HttpResponse("AgregarRecetas")

def editarRecetas(request):
    return HttpResponse("EditarRecetas")

def buscarRecetas(request):
    ingredientes = request.GET.get('ingredientes', '')
    recetas = buscar_recetas_ingredientes(ingredientes, num_recetas=10)
    favoritos_ids = Favoritos.objects.filter(usuario=request.user).values_list('url_id_receta', flat=True) if request.user.is_authenticated else []
    context = {'recetas': recetas, 'favoritos_ids': favoritos_ids, 'username': nombre_usuario(request)}
    return render(request, "recetas/buscarRecetas.html", context)

@login_required
def toggle_favorito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receta_id = data.get('receta_id')
        receta_titulo = data.get('receta_titulo')
        receta_imagen = data.get('receta_imagen')
        receta_url = data.get('receta_url')  # Obtener la URL de la receta
        is_checked = data.get('is_checked')

        if is_checked:
            Favoritos.objects.create(
                usuario=request.user,
                titulo=receta_titulo,
                url_id_receta=receta_url,  # Guardar la URL de la receta
                img=receta_imagen,
            )
            message = "Receta añadida a favoritos"
        else:
            Favoritos.objects.filter(usuario=request.user, url_id_receta=receta_url).delete()
            message = "Receta eliminada de favoritos"

        return JsonResponse({'message': message})

def guardarRecetas(request):
    return HttpResponse("GuardarRecetas")

def verNutricional(request):
    return HttpResponse("VerNutricional")

def filtrarRecetas(request):
    # Obtener los parámetros de búsqueda
    ingredientes = request.GET.get('ingredientes', '')
    diet = request.GET.get('diet', '')
    health = request.GET.get('health', '')
    cuisineType = request.GET.get('cuisineType', '')
    mealType = request.GET.get('mealType', '')
    dishType = request.GET.get('dishType', '')
    calories_min = request.GET.get('calories_min', '')
    calories_max = request.GET.get('calories_max', '')
    time = request.GET.get('time', '')

    # Llamar a la función que obtiene las recetas de la API
    recetas = obtener_recetas(ingredientes, diet, health, cuisineType, mealType, dishType, calories_min, calories_max, time)
    
    return render(request, 'recetas/filtrarRecetas.html', {'recetas': recetas, 'username': nombre_usuario(request)})
