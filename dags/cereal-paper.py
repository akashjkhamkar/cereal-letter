from datetime import date
from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago

from cereal_paper_src.news import get_news
from cereal_paper_src.joke import get_joke
from cereal_paper_src.quote import get_quote
from cereal_paper_src.combine import combine_articles
from cereal_paper_src.song import get_song, get_songs_from_db
from cereal_paper_src.meme import get_meme
from cereal_paper_src.pdf import create_pdf
from cereal_paper_src.mongo_utils import save_to_db

default_args = {
    'owner': 'akashk',
    'depends_on_past': False,
    'email': 'cerealman@akashkhamkar.in',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': None
}

dag = DAG(
    'cereal_paper',
    default_args=default_args,
    description='A DAG to fetch interesting stuff from a collection of open apis and send user a paper made out of it.',
    start_date=days_ago(1),
    tags=['automationwithairflow'],
    render_template_as_native_obj=True,
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

extraction_tasks.append(PythonOperator(
    task_id='get_songs_from_db_task',
    python_callable=get_songs_from_db,
    dag=dag
))

combine_all_articles = PythonOperator(
    task_id='combine_articles_task', 
    python_callable=combine_articles,
    provide_context=True,
    dag=dag
)

save_letter_to_db = PythonOperator(
    task_id='save_to_db_task',
    python_callable=save_to_db,
    provide_context=True,
    dag=dag
)

create_the_letter_pdf = PythonOperator(
    task_id='create_pdf_task',
    python_callable=create_pdf,
    provide_context=True,
    dag=dag
)

send_email = EmailOperator( 
    task_id='send_email', 
    to='akash.khamkar40@gmail.com', 
    subject='Cereal letter | ' + str(date.today()),
    html_content="Top of the morning, your todays cereal letter is here. ",
    files=["{{ task_instance.xcom_pull(task_ids='create_pdf_task') }}"],
    dag=dag
)

extraction_tasks >> combine_all_articles >> [create_the_letter_pdf, save_letter_to_db]
create_the_letter_pdf >> send_email