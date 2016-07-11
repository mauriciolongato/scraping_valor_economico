import bs4
from urllib.request import urlopen
import time


def get_noticia_valor_economico(html):
    noticia = {}
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
        # print (tags.get_text())
    except:
        noticia['tags'] = ''

    # Corpo do texto
    try:
        noticia['texto_corpo'] = soup.find ('div', title=False, class_="node-body").get_text ()
        # print (texto_corpo.get_text())
    except:
        noticia['texto_corpo'] = ''

    return noticia


if __name__ == '__main__':
    # Pagina exemplo
    conn = sql.connect('Noticias_Raw_DB.db')
    cur = conn.cursor()
    noticia = cur.execute("SELECT * FROM _20160711_Noticias;")

    cols = ['url', 'extraction_date', 'extraction_time', 'html_info', 'processing_status']
    noticia_pd = pd.DataFrame.from_records(data=noticia.fetchall(), columns=cols)

    conn.commit()
    conn.close()

    print(noticia_pd['html_info'][0])