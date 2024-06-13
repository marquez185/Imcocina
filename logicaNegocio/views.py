import requests
from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup

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

def index(request):
    news = fetch_bbc_news()
    return render(request, "logicaNegocio/index.html", {'news': news})