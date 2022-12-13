from pymongo import MongoClient

def get_database():
   CONNECTION_STRING = "mongodb://mongodb/cereal_db"
   client = MongoClient(CONNECTION_STRING)
   return client['cereal_db']

def save_to_db(**context):
    letter = context['ti'].xcom_pull(task_ids='combine_articles_task')

    cereal_db = get_database()
    letters = cereal_db["letters"]

    letters.insert_one(letter)
