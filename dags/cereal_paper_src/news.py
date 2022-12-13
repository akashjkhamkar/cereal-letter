import requests
import json

max_number_of_news = 3

def get_news():
    res = requests.get('https://newsdata.io/api/1/news?apikey=pub_14522263f5b506fbc598ba7459459c982de1f&language=en&category=top,technology,science&page=1')

    if res.status_code != 200:
        return f'No news for you today, news api is having some mid life crisis  .'

    news = json.loads(res.text)
    
    result = []
    for article in news['results'][:max_number_of_news]:
        new_article = {}

        new_article['title'] = str(article['title'])
        new_article['published_date'] = str(article['pubDate'])
        new_article['summary'] = str(article['description'])
        
        result.append(new_article)

    return result