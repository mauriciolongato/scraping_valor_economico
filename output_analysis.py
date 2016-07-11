import sqlite3 as sql
import pandas as pd
import bs4

# Conecta no banco e pega os dados
conn = sql.connect('Noticias_Raw_DB.db')
cur = conn.cursor()
noticia = cur.execute("SELECT * FROM _20160711_Noticias;")

cols = ['url', 'extraction_date', 'extraction_time', 'html_info', 'processing_status']
noticias = pd.DataFrame.from_records(data=noticia.fetchall(), columns=cols)

conn.commit()
conn.close()

# Inicia o tratamento do html


# noticias['soup_info'] = [bs4.BeautifulSoup(html, "lxml") for html in list(noticias['html_info'])]

# print(noticias['soup_info'].get_text())