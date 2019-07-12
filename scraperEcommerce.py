#!/usr/bin/env python
# coding: utf-8
## @Tiago de Camargo::
### github - https://github.com/ticamargo
### linkedin - https://www.linkedin.com/in/tiagodecamargo/


## IMPORT DE PACOTES
import requests
from datetime import date
import time
import pandas as pd
from bs4 import BeautifulSoup


##### ## INICIAR VARIAVEIS ######
hoje = date.today()
iter_url = 0
total = []
dados = ''


## URL PRINCIPAL PARA CONSULTAS - URL 1.a PAGINA E URL2 2.a PAGINA EM DIANTE ACRESCENTANDO OFFSET 24 EM 24.
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url = 'https://americanas.com.br/busca/523'


for i in range(13):
    time.sleep(10)
    if i != 0:
        iter_url += 24
        response = requests.request("GET", 'https://americanas.com.br/busca/523?limite=24&offset='+str(iter_url)+'', headers=headers)
        dados += str(response.text)
    else:
        response = requests.request("GET", url, headers=headers)
        dados += str(response.text)


## GRAVAR DADOS DAS REQUISIÇÕES HTTP DO SITE
with open('html_paginas_'+str(hoje)+'.html', encoding='UTF-8', mode="w+") as arquivo:
    arquivo.write(dados)

 
## TRANSFORMAR EM OBJETO BS4
soup = BeautifulSoup(dados, 'html.parser')


## BUSCAR GRADE DE PRODUTOS PELATAG FIX DE TODAS AS PAGINAS
lista_produtos = soup.find_all('div', class_="product-grid-item ColUI-sc-1ey7nd2-0 fUgyk ViewUI-oocyw8-6 kvewNe")


## FUNCOES DE LIMPEZA PARA CADA PRODUTO APRESENTADO NA GRID DE BUSCA
def funcLenght6 (posicao_produto):
    p1 = lista_produtos[posicao_produto].section.text.split(",")
    temp_centavos = ("," + (p1[-1])[:2])
    del p1[-1]
    temp_url = p1[-1].split('}')
    temp_preco = p1[-1].split(' deR$ ')
    del p1[-1]
    p1.append(temp_url[0])
    p1.append(temp_preco[-1]+temp_centavos)
    del p1[0:2]
    total.append(p1)


def funcLenght7 (posicao_produto):
    p2 = lista_produtos[posicao_produto].section.text.split(",")
    del p2[-1]
    temp_centavos = ("," + (p2[-1])[:2])
    del p2[-1]
    temp_preco = p2[-1].split(' deR$ ')
    temp_url = p2[-1].split('}')
    del p2[-1]
    p2.append(temp_url[0])
    p2.append(temp_preco[-1]+temp_centavos)
    del p2[0:2]
    total.append(p2)


def funcLenght10 (posicao_produto):
    p3 = lista_produtos[posicao_produto].section.text.split(",")
    del p3[-1]
    temp_centavos = ("," + (p3[-1])[:2])
    del p3[-1]
    p3[-1]
    temp = p3[-1].split(' deR$ ')
    p3[-1] = temp[0]
    p3.append(temp[-1]+temp_centavos)
    del p3[5:8]
    del p3[0:2]
    total.append(p3)


#####   CHAMAR FUNCOES PARA LIMPEZA E CARREGAMENTO EM LISTA DEFINITVA
def iniciaLimpeza():
    for i in range(len(lista_produtos)):
        teste_len = lista_produtos[i].section.text.split(",")
#        print(i, 'Tamanho: ', len(teste_len))
        if len(teste_len) == 6:
            funcLenght6(i)
        elif len(teste_len) == 7:
            funcLenght7(i)
        elif len(teste_len) == 10:
            funcLenght10(i)
        else: continue

    
## CHAMA METODO CORRESPONDENTE
iniciaLimpeza()


## FILTRA PARA DATAFRAME
df = pd.DataFrame(total)


## SETA COLUNAS
df.columns=['nome', 'imagem', 'url', 'preco']
df.loc[0:, 'nome'] = df['nome'].map(lambda d: "{}".format(d[8:]))
df.loc[0:, 'imagem'] = df['imagem'].map(lambda d: "{}".format(d[19:]))
df.loc[0:, 'url'] = df['url'].map(lambda d: "{}".format(d[7:]))
df.loc[0:, 'url'] = df['url'].map(lambda d: "{}".format("https://www.americanas.com.br" + d ))
df['nome'] = df['nome'].apply(lambda x: x.replace('"',''))
df['url'] = df['url'].apply(lambda x: x.replace('"',''))
df['imagem'] = df['imagem'].apply(lambda x: x.replace('"',''))
df['imagem'] = df['imagem'].apply(lambda x: x.replace('}',''))


## GRAVA ARQUIVO EXCEL
with pd.ExcelWriter(r'523americanas.xlsx') as writer:
    df.to_excel(writer, sheet_name='LinkseURLs', engine='xlsxwriter', index=False)
