from fpdf import FPDF
from datetime import date

title = 'Cereal Paper'
todays_date = str(date.today())
logo = './dags/morning_paper_src/logo.png'

def convert_date(date_string):
    return date_string[2:]

def h1(pdf, text):
    pdf.set_font_size(20)
    pdf.cell(200, 10, txt = text, ln = 1, align = 'C')

def h3(pdf, text):
    pdf.set_font_size(16)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(200, 10, txt = text, ln = 1, align = 'L')

def centered_regular(pdf, text):
    pdf.set_font_size(10)
    pdf.cell(200, 10, txt = text, ln = 1, align = 'C')

def regular(pdf, text):
    pdf.set_font_size(10)
    pdf.multi_cell(0, 5, text, 0, 1)

def footer(pdf, text):
    pdf.set_font_size(16)
    pdf.cell(200, 10, txt = text, ln = 1, align = 'C')

def create_pdf(**context):
    pdf = FPDF()
    
    pdf.add_font('SpecialElite', '', '/opt/airflow/dags/morning_paper_src/SpecialElite.ttf', uni=True)
    pdf.set_font('SpecialElite', '', 12)
    pdf.add_page()
    pdf.set_title(title)

    article = context['ti'].xcom_pull(task_ids='combine_articles_task')

    # Adding title
    h1(pdf, title)
    centered_regular(pdf, convert_date(todays_date))
    pdf.ln(4)

    pdf.ln(10)
    pdf.image(logo, x = 7, y = 3, w = 30, h = 30)

    # News
    h3(pdf, 'Todays headlines')

    if isinstance(article['news'], str):
        regular(pdf, article['news'])
    else:
        for i, news in enumerate(article['news']):
            regular(pdf, str(i + 1) + ".")
            regular(pdf, 'Title : ' + news['title'])
            regular(pdf, 'Date : ' + convert_date(news['published_date']))
            regular(pdf, 'Summary : ' + news['summary'].replace('\n', ' '))
            pdf.ln(2)

    pdf.ln(4)

    # Joke
    h3(pdf, 'A joke to tickle your bones')
    regular(pdf, article['joke'])
    pdf.ln(4)

    # Quote
    h3(pdf, 'Some deep stuff')
    regular(pdf, article['quote'])
    pdf.ln(4)

    # Songs
    h3(pdf, 'Todays song recommendations by akash')
    for song in article['songs']:
        regular(pdf, "Song : " + song[0])
        regular(pdf, "Album : " + song[1])
        regular(pdf, "Artists : " + song[2])
        pdf.ln(2)

    footer(pdf, "*    *    *")
    pdf.output('./temp/cereal_paper.pdf', 'F')