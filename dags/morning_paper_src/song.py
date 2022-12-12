import requests
import json
import random

def get_song():
    song_id = random.randrange(2000000)
    # token = 'aKtb2wbRd1TFLuMoxaekQ1x6yPCu8B9971-rSOvLlnI79U_Ie-RbLsHkLIlphNyu'
    token = "?access_token=CXyFeSBw2lAdG41xkuU3LS6a_nwyxwwCz2dCkUohw-rw0C49x2HqP__6_4is5RPx"
    song_url = 'https://api.genius.com/songs/' + str(song_id) + token
    
    res = requests.get(song_url)

    if res.status_code != 200:
        print('response **** ', res.text)
        return f'Music api failed with response code {res.status_code} .'

    song_dict = json.loads(res.text)

    print(song_dict)
    return song_dict
