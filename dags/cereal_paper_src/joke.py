import requests
import json

def get_joke():
    res = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,explicit&type=single')

    if res.status_code != 200:
        return f'Joke api failed with response code {res.status_code} .'

    joke_dict = json.loads(res.text)

    print(joke_dict)
    return joke_dict['joke']