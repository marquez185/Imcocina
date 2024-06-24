import requests
import json
import os
from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup
from googlesearch import search
from recetas import API_recetas as API


def fetch_bbc_news():
    url = 'https://www.bbc.com/mundo/topics/cdr5617v8d8t'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_list = []
    articles = soup.select('.bbc-t44f9r')[:6]  # Limita a las primeras 4 noticias

    for article in articles:
        title = article.find('h2').text
        link = article.find('a')['href']
        if not link.startswith('https://www.bbc.com'):
            full_link = f"https://www.bbc.com{link}"
        else:
            full_link = link
        image_url = article.find('img')['src']
        description = article.find('p').text if article.find('p') else 'No description available'
        pub_date = article.find('time')['datetime'] if article.find('time') else None

        news_item = {
            'title': title,
            'image_url': image_url,
            'description': description,
            'link': full_link,
            'pub_date': pub_date
        }
        news_list.append(news_item)

    return news_list

def search_tips():
    waste_reduction_query = "Consejos de la reducción de desperdicio en alimentos"
    food_utilization_query = "Cómo aprovechar todos los alimentos"
    
    waste_reduction_results = []
    food_utilization_results = []

    # Supongamos que tienes una función `search` que obtiene enlaces basados en la query
    for link in search(waste_reduction_query, num_results=2, lang="es"):
        waste_reduction_results.append(link)

    for link in search(food_utilization_query, num_results=4, lang="es"):
        food_utilization_results.append(link)
    
    return waste_reduction_results, food_utilization_results

def fetch_search_results(links):
    search_results = []
    default_image = '/static/logicaNegocio/img/desperdicio_comida.webp'

    for url in links:
        result = {'url': url, 'title': '', 'image': default_image}

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Obtener título
                title_tag = soup.find('title')
                if title_tag:
                    result['title'] = title_tag.text

                # Obtener imagen
                image_tag = soup.find('img', src=True)
                if image_tag:
                    img_src = image_tag['src']
                    if img_src.endswith('.webp'):
                        result['image'] = img_src
        except Exception as e:
            print(f"Error fetching {url}: {e}")

        search_results.append(result)
    
    return search_results

def save_results_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_results_from_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

'''MANEJO DE NOMBRE DE SESION'''

def nombre_usuario(request):
    if request.user.is_authenticated:
        return request.user.first_name
    return None
    
'''LOGICA DE LAS TEMPLATE'''

def index(request):
    recetas = API.buscar_recetas_aleatorias(num_recetas=5)
    context = {
        'recetas': recetas,
        'username': nombre_usuario(request)  # Llamar a la función correctamente
    }
    return render(request, "logicaNegocio/index.html", context)

def noticias(request):
    news = fetch_bbc_news()
    return render(request, "logicaNegocio/noticias.html", {
        'news': news,
        'username': nombre_usuario(request)
    })

def desperdicio(request):
    json_filename = 'search_results.json'
    
    # Cargar resultados desde el archivo JSON si existe
    cached_results = load_results_from_json(json_filename)
    waste_reduction_results = cached_results.get('waste_reduction_results', [])
    food_utilization_results = cached_results.get('food_utilization_results', [])

    if not waste_reduction_results or not food_utilization_results:
        waste_reduction_links, food_utilization_links = search_tips()

        waste_reduction_results = fetch_search_results(waste_reduction_links)
        food_utilization_results = fetch_search_results(food_utilization_links)

        # Guardar los resultados en el archivo JSON
        results_to_save = {
            'waste_reduction_results': waste_reduction_results,
            'food_utilization_results': food_utilization_results
        }
        save_results_to_json(json_filename, results_to_save)

    context = {
        'waste_reduction_results': waste_reduction_results,
        'food_utilization_results': food_utilization_results,
    }

    return render(request, 'logicaNegocio/desperdicio.html', context)


def nosotros(request):
    return render(request, "logicaNegocio/nosotros.html", {'username': nombre_usuario(request)})

def politicas_privacidad(request):
    return render(request, 'logicaNegocio/politicas_privacidad.html')

def terminos_uso(request):
    return render(request, 'logicaNegocio/terminos_uso.html')
