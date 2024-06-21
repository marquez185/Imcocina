import requests
from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup
from googlesearch import search


def fetch_bbc_news():
    url = 'https://www.bbc.com/mundo/topics/cdr5617v8d8t'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_list = []
    articles = soup.select('.bbc-t44f9r')[:4]  # Limita a las primeras 4 noticias

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

# search_tips.py
def search_tips():
    waste_reduction_query = "Consejos de la reducción de desperdicio en alimentos"
    food_utilization_query = "Cómo aprovechar todos los alimentos"
    
    waste_reduction_results = []
    food_utilization_results = []

    for link in search(waste_reduction_query, num_results=2, lang="es"):
        waste_reduction_results.append(link)

    for link in search(food_utilization_query, num_results=4, lang="es"):
        food_utilization_results.append(link)
    
    return waste_reduction_results, food_utilization_results


def index(request):
    news = fetch_bbc_news()
    waste_reduction_links, food_utilization_links = search_tips()
    return render(request, "logicaNegocio/index.html", {
        'news': news,
        'waste_reduction_links': waste_reduction_links,
        'food_utilization_links': food_utilization_links,
    })

def nosotros(request):
    return render(request, "logicaNegocio/nosotros.html")