import requests
import json

def get_news():
    res = requests.get('https://newsdata.io/api/1/news?apikey=pub_14522263f5b506fbc598ba7459459c982de1f&language=en&country=in&page=1')

    if res.status_code != 200:
        return f'No news for you today, news api is having some mid life crisis  .'

    news = json.loads(res.text)
    
    result = []
    for article in news['results'][:3]:
        new_article = {}

        new_article['title'] = str(article['title'])
        new_article['published_date'] = str(article['pubDate'])
        new_article['summary'] = str(article['description'])
        
        result.append(new_article)

    return result