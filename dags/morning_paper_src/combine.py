def combine_articles(**context):
    article = {}

    article['joke'] = context['ti'].xcom_pull(task_ids='get_joke_task')
    article['quote'] = context['ti'].xcom_pull(task_ids='get_quote_task')
    article['news'] = context['ti'].xcom_pull(task_ids='get_news_task')
    article['meme'] = context['ti'].xcom_pull(task_ids='get_meme_task')

    print(article)
    return article
