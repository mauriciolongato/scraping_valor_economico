import bs4
import crawler_html as c_html
from urllib.request import urlopen


# obtem lista de links da pagina do valor
from scraping_valor_economico.crawler_html import get_html_to_DB

url_valor_impresso = 'http://www.valor.com.br/impresso'
html = urlopen (url_valor_impresso)
soup = bs4.BeautifulSoup (html, 'lxml')

# Busca os links das noticias na pagina principal
url_base = 'http://www.valor.com.br'
links_alor = soup.find_all ('a', title=False, href=True, class_="valor-impresso-indice-node-title")
urls = [url_base+link['href'] for link in links_alor]

# Faz a requisicao das informacoes do html
[c_html.get_html_to_DB(url, 'Noticias_Raw_DB', '_20160711_Noticias') for url in urls]
