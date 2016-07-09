from bs4 import BeautifulSoup
import json
import requests
import urllib
import time
import sqlite3 as sql
import pandas as pd
from IPython.display import HTML

#Scraping de uma unica noticia
url = 'http://www.valor.com.br/impresso'

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

#Scraping main page Valor Economico
noticias_capa  = soup.find_all("h2", class_="manchete-title title2 valor-impresso-indice-node-title inline")    #Noticias Capa

#Obtem os titulos das noticias da capa
prefix = 'http://www.valor.com.br/'
lista_noticias ={}
for element in noticias_capa:
    titulo = element.a.get_text().encode('cp1252')    #Titulo da noticia da capa
    url    = prefix + element.a["href"]                #url da noticia da capa
    lista_noticias[titulo] = {'url':url}

print("carregadas urls: ",len(lista_noticias.keys()))

for key, url in zip(lista_noticias.keys()[0:3],lista_noticias.values()[0:3]):
    html = urllib.urlopen(url['url']).read()
    soup = BeautifulSoup(html)

    #Tratamentos
    #Secao
    try:
        section = soup.find_all("a", class_="active")[0].get_text().encode('cp1252')
    except:
        section = []
    #Tags
    try:
        tags = soup.find_all("div",  class_="tag-list block")[0]
        tag_list = [tag.get_text('a').encode('cp1252').replace('  ','').replace('\n','') for tag in tags.find_all('a')]
    except:
        tag_list =[]
    #Texto
    try:
        textos = soup.find_all("div",  class_="n-content")[0]
        texto_list = [texto.get_text('p').encode('cp1252') for texto in textos.find_all('p')]
        texto_noticia = texto_list
        if texto_noticia == ['']:
            try:
                texto_list = soup.find_all("div",  class_="node-body")[0].get_text().encode('cp1252')
                texto_noticia = [texto_list]
            except:
                texto_noticia = ['']
    except:
        texto_noticia =['']
    #Titulo
    try:
        titulo = [soup.find_all("h1",   class_="title1")[0].get_text().encode('cp1252')]
    except:

        titulo = ['']
    #Data publicacao
    try:
        data_publicacao = soup.find_all("span", class_="date submitted")[0].get_text().encode('cp1252')
    except:
        data_publicacao = ''
    # Data de extracao

    #print "informacoes extraidas: ",data_publicacao,time.strftime("%d/%m/%Y"),time.strftime("%H:%M:%S"),section,titulo, tag_list, texto_noticia
    #obtem informacoes
    print(lista_noticias[key])
    lista_noticias[key]['Data_publicacao'] = data_publicacao                                 #Data
    lista_noticias[key]['Data_Extracao']   = time.strftime("%d/%m/%Y")                         #Dia da extracao
    lista_noticias[key]['Hora_Extracao']   = time.strftime("%H:%M:%S")                         #Dia da extracao
    lista_noticias[key]['Secao']           = section                                          #Secao em que a noticia foi publicada
    lista_noticias[key]['Titulo']          = titulo                                            #Titulo
    lista_noticias[key]['Tags']            = tag_list                                          #Tags
    lista_noticias[key]['Conteudo']        = texto_noticia                                     #Resumo

#cols = ['Data_publicacao', 'Data_Extracao', 'Hora_Extracao', 'Secao', 'Url', 'Titulo', 'Tags', 'Conteudo']
count = 0
for noticia in lista_noticias:
    try:
        print(lista_noticias[noticia]['Conteudo'])
        print(lista_noticias[noticia])
    except:
        pass
lista_noticias_pd = pd.DataFrame.from_dict(data = lista_noticias, orient='index')
lista_noticias_pd.to_csv('20160708_Valor_PP.csv')


#Insere dados do DB_valor
#cria a tabela
conn = sql.connect('20160708_Noticias_Valor.db')
conn.text_factory = str
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Noticias;")
cur.execute('''CREATE TABLE Noticias(
                     data_publicacao  VARCHAR(50)
                    ,data_extracao    VARCHAR(50)
                    ,hora_extracao    VARCHAR(50)
                    ,secao            VARCHAR(20)
                    ,url              VARCHAR(1000)
                    ,titulo           VARCHAR(300)
                    ,tags             VARCHAR(1000)
                    ,conteudo         VARCHAR(5000)

    );''')


# Insere valores
for noticia in lista_noticias:
    row = [lista_noticias[noticia]['Data_publicacao'] ,lista_noticias[noticia]['Data_Extracao'], lista_noticias[noticia]['Hora_Extracao'], lista_noticias[noticia]['Secao'] ,noticia, lista_noticias[noticia]['Titulo'] ,lista_noticias[noticia]['Tags'], lista_noticias[noticia]['Conteudo']]
    cur.executemany('''INSERT INTO Noticias VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', [row])


conn.commit()
conn.close()


