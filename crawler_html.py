import sqlite3 as sql
import bs4
import pandas as pd
from urllib.request import urlopen
import time


def get_html_to_DB(url, nome_db, nome_tbl):
    html = urlopen(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    extraction_date = time.strftime("%d/%m/%Y")
    extraction_time = time.strftime("%H:%M:%S")

    conn = sql.connect(nome_db + '.db')

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS {};".format(nome_tbl))
    cur.execute("""CREATE TABLE {} (
                         url                TEXT
                        ,extraction_date    TEXT
                        ,extraction_time    TEXT
                        ,html_info          TEXT
                        ,processing_status  INTEGER

        );""".format(nome_tbl))

    cur.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?);'.format(nome_tbl),
                [url, extraction_date, extraction_time, soup.get_text(), 0])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Pagina exemplo
    url = 'http://www.valor.com.br/politica/4629309/fhc-e-internado-em-sao-paulo-para-colocar-marca-passo'
    get_html_to_DB(url, 'Noticias_Raw_DB', 'extraction_info')

    # Leitura exemplo DB
    conn = sql.connect('Noticias_Raw_DB.db')
    cur = conn.cursor()
    noticia = cur.execute("SELECT * FROM extraction_info;")

    cols = ['url', 'extraction_date', 'extraction_time', 'html_info', 'processing_status']
    noticia_pd = pd.DataFrame.from_records(data = noticia.fetchall(), columns = cols)

    conn.commit()
    conn.close()

    # print(noticia_pd['html_info'][0])
