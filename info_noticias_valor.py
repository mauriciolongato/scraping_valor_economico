import bs4
from urllib.request import urlopen
import time
import re


def get_noticia_valor_economico(url, nome_db=None, nome_tbl=None):
    noticia = {}
    html = urlopen (url)
    soup = bs4.BeautifulSoup (html, 'lxml')

    noticia['url'] = url
    # data da extracao da informacao
    noticia['data_extracao'] = time.strftime ("%d/%m/%Y")
    noticia['hora_extracao'] = time.strftime ("%H:%M:%S")

    # Obtem caderno
    try:
        noticia['caderno'] = soup.find ('a', title=True, class_="active").get_text ()
        # print (caderno.get_text ())
    except:
        noticia['caderno'] = ''

    # Obtem data publicacao
    try:
        noticia['data_publicacao'] = soup.find ('span', title=False, class_="date submitted").get_text ()
        # print (data.get_text ())
    except:
        noticia['data_publicacao'] = ''

    # Titulo noticia
    try:
        noticia['titulo'] = soup.find ('h1', title=False, class_="title1").get_text ()
        # print (titulo.get_text ())
    except:
        noticia['titulo'] = ''

    # Obtem tags
    try:
        noticia['tags'] = soup.find ('div', title=False, class_="tags").get_text ()
        print ("tags: ", noticia['tags'])
    except:
        noticia['tags'] = ''

    # Corpo do texto
    try:
        noticia['texto_corpo'] = soup.find ('div', title=False, class_="node-body").get_text ()
        # print (texto_corpo.get_text())
    except:
        noticia['texto_corpo'] = ''

    if nome_db != None and nome_tbl != None:
        return 0
    # print (noticia)
    return noticia


if __name__ == '__main__':
    # Pagina exemplo
    url = 'http://www.valor.com.br/politica/4629309/fhc-e-internado-em-sao-paulo-para-colocar-marca-passo'
    info = get_noticia_valor_economico (url)
    print (info['tags'].replace ('  ', '').replace ('\n\n', ';'))
    # [v for v in (' '.join([u for u in noticia['tags'].split(' ') if u != ''])).split('\n') if v != '']