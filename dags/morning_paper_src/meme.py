import base64
import requests
import json

def get_meme():
    url = 'https://meme-api.com/gimme'

    res = requests.get(url)

    if res.status_code != 200:
        return 'Meme api failed, laugh again later : code - ' + res.status_code
    
    result = json.loads(res.text)
    return result['postLink']