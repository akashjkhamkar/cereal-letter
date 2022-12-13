import requests
import json
import random
from airflow.hooks.postgres_hook import PostgresHook

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

def get_songs_from_db():
    ids = [random.randrange(100) for i in range(3)]
    query = 'SELECT "Track Name", "Album Name", "Artist Names" FROM songs WHERE id IN ({}, {}, {})'.format(ids[0], ids[1], ids[2])

    pg_hook = PostgresHook(
        postgres_conn_id='postgres_default',
        schema='airflow'
    )
    
    pg_conn = pg_hook.get_conn()
    cursor = pg_conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()