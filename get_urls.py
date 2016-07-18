import datetime
import bs4
import json
from urllib.request import urlopen
import pandas as pd


# Cria a lista com as datas dos ultimos numdays que queremos analisar do site
base = datetime.datetime.today()
numdays = 365
date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
urls_do_dia = {}

for date in date_list:
    # Cria os valores das datas para acrescentar na URL
    date_str = str(date.strftime('%Y%m%d'))

    # obtem lista de links da pagina do valor
    url_valor_impresso = 'http://www.valor.com.br/impresso/{0}'.format(date_str)
    html = urlopen (url_valor_impresso)
    soup = bs4.BeautifulSoup (html, 'lxml')

    # Busca os links das noticias na pagina principal
    url_base = 'http://www.valor.com.br'
    links_valor = soup.find_all ('a', title=False, href=True, class_="valor-impresso-indice-node-title")
    urls = [url_base+link['href'] for link in links_valor]


    urls_do_dia[date_str] = urls
    print(date_str, len(urls))

with open('{0}_{1}_urls_valor_economico.txt'.format(base.strftime('%Y%m%d'), date_str), 'w') as outfile:
    json.dump(urls_do_dia, outfile)

