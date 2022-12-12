import json
import requests
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago

from morning_paper_src.news import get_news
from morning_paper_src.joke import get_joke
from morning_paper_src.quote import get_quote
from morning_paper_src.combine import combine_articles
from morning_paper_src.song import get_song
from morning_paper_src.meme import get_meme
from morning_paper_src.pdf import create_pdf

default_args = {
    'owner': 'akashk',
    'depends_on_past': False,
    'email': ['akash.khamkar40@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': None
}

dag = DAG(
    'daily_paper',
    default_args=default_args,
    description='A DAG to fetch interesting stuff from a collection of open apis and send user a paper made out of it.',
    start_date=days_ago(1),
    tags=['automationwithairflow'],
)

extraction_tasks = []

extraction_tasks.append(PythonOperator(
    task_id='get_joke_task', 
    python_callable=get_joke,
    dag=dag
))

extraction_tasks.append(PythonOperator(
    task_id='get_quote_task',
    python_callable=get_quote,
    dag=dag
))

extraction_tasks.append(PythonOperator(
    task_id='get_news_task',
    python_callable=get_news,
    dag=dag
))

# Genius api failing only in airflow for some reason
# extraction_tasks.append(PythonOperator(
#     task_id='get_song_task',
#     python_callable=get_song,
#     dag=dag
# ))

extraction_tasks.append(PythonOperator(
    task_id='get_meme_task',
    python_callable=get_meme,
    dag=dag
))

combine_articles = PythonOperator(
    task_id='combine_articles_task', 
    python_callable=combine_articles,
    provide_context=True,
    dag=dag
)

create_pdf = PythonOperator(
    task_id='create_pdf_task',
    python_callable=create_pdf,
    provide_context=True,
    dag=dag
)

extraction_tasks >> combine_articles >> create_pdf
