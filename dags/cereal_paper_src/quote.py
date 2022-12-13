import requests
import json

def get_quote():
    res = requests.get('https://zenquotes.io/api/today')

    if res.status_code != 200:
        return f'Quotes api failed with response code {res.status_code} .'

    quotes = json.loads(res.text)
    print(quotes)
    return quotes[0]['q']