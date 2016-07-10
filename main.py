import bs4
from urllib.request import urlopen
import info_noticias_valor as iv
import pandas as pd


# obtem lista de links da pagina do valor
url_valor_impresso = 'http://www.valor.com.br/impresso'
html = urlopen (url_valor_impresso)
soup = bs4.BeautifulSoup (html, 'lxml')

# Busca os links das noticias na pagina principal
url_base = 'http://www.valor.com.br'
links_alor = soup.find_all ('a', title=False, href=True, class_="valor-impresso-indice-node-title")
urls = [url_base+link['href'] for link in links_alor]


# Obtem as informacoes de cada noticia
noticias = {}
for url in urls:
    noticias[url] = iv.get_noticia_valor_economico(url)
