import json
import crawler_html as ch
import bs4
from urllib.request import urlopen


with open('20160717_20150719_urls_valor_economico.txt') as json_data:
    d = json.load(json_data)
    json_data.close()

ch.create_DB('Valor_Economico', 'html_20160717_20150719')

htmls = {}
for date in d.keys():
    url_html = {}
    for url_news in d[date]:
        html = urlopen (url_news)
        soup = bs4.BeautifulSoup (html, 'lxml')
        url_html[url_news] = soup.get_text()

    htmls[date] = url_html

    address = 'C:\\Users\\Mauricio\\PycharmProjects\\Scraping_Valor_Economico\\output\\'
    with open(address+'{0}_htmls_valor_economico.txt'.format(date), 'w') as outfile:
        json.dump(htmls, outfile)



