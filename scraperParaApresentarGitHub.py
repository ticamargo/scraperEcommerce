{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/usr/bin/env python\n",
    "# coding: utf-8\n",
    "## @Tiago de Camargo::\n",
    "### github - https://github.com/ticamargo\n",
    "### linkedin - https://www.linkedin.com/in/tiagodecamargo/"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## IMPORT DE PACOTES\n",
    "import requests\n",
    "from datetime import date\n",
    "import time\n",
    "import xlsxwriter\n",
    "import csv\n",
    "import pandas as pd\n",
    "from bs4 import BeautifulSoup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "##### ## INICIAR VARIAVEIS ######\n",
    "hoje = date.today()\n",
    "iter_url = 0\n",
    "total = []\n",
    "dados = ''"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## URL PRINCIPAL PARA CONSULTAS - URL 1.a PAGINA E URL2 2.a PAGINA EM DIANTE ACRESCENTANDO OFFSET 24 EM 24.\n",
    "headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'}\n",
    "url = 'url do ecommerce'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for i in range(13):\n",
    "    time.sleep(10)\n",
    "    if i != 0:\n",
    "        iter_url += 24\n",
    "        response = requests.request(\"GET\", 'url mais o pula pagina'+str(iter_url)+'', headers=headers)\n",
    "        dados += str(response.text)\n",
    "    else:\n",
    "        response = requests.request(\"GET\", url, headers=headers)\n",
    "        dados += str(response.text)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## GRAVAR DADOS DAS REQUISIÇÕES HTTP DO SITE\n",
    "with open('html_paginas_'+str(hoje)+'.html', encoding='UTF-8', mode=\"w+\") as arquivo:\n",
    "    arquivo.write(dados)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## LER LOCAL PARA TESTE\n",
    "with open('html_paginas_2019-09-02.html', encoding='UTF-8', mode=\"r\") as arquivo:\n",
    "    dados = arquivo.read()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## TRANSFORMAR EM OBJETO BS4\n",
    "soup = BeautifulSoup(dados, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ACHAR TAG DOS PRODUTOS\n",
    "tagProduto = 'product-grid-item ColUI-'\n",
    "acheiProdutos = dados.find(tagProduto)\n",
    "print(acheiProdutos)\n",
    "tagClass = dados[acheiProdutos:acheiProdutos+66]\n",
    "print(tagClass)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "lista_produtos = soup.find_all('div', class_=tagClass)\n",
    "print(len(lista_produtos))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## RECEBER STRING\n",
    "paraProcurar = str(lista_produtos[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ACHAR TAG DO NOME DO PRODUTO\n",
    "tagNome = 'TitleWrapper-'\n",
    "acheiNome = paraProcurar.find(tagNome)\n",
    "print(acheiNome)\n",
    "tagClassNome = paraProcurar[acheiNome:acheiNome+59]\n",
    "print(tagClassNome)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ACHAR TAG DO PRECO DO PRODUTO\n",
    "tagPreco = 'PriceWrapper-'\n",
    "acheiPreco = paraProcurar.find(tagPreco)\n",
    "print(acheiPreco)\n",
    "tagClassPreco = paraProcurar[acheiPreco:acheiPreco+56]\n",
    "print(tagClassPreco)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## OK"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "## ORGANIZA OS DADOS EM LISTA\n",
    "lista, lista_temp = [],[]\n",
    "for i in range(len(lista_produtos)):\n",
    "    try:\n",
    "        url = str(lista_produtos[i].a).split('><')\n",
    "        #print(url[0])\n",
    "        nome = lista_produtos[i].find(class_=tagClassNome).get_text()\n",
    "        #print(nome)\n",
    "        preco = lista_produtos[i].find(class_=tagClassPreco).get_text()\n",
    "        #print(preco)\n",
    "    except Exception:\n",
    "        preco = '0,00'\n",
    "    lista_temp = [url[0], nome, preco]\n",
    "    lista.append(lista_temp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Verificar erros\n",
    "#lista[53]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## DE CIMA OK"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(len(lista))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## VER LISTA\n",
    "lista"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## FILTRA PARA DATAFRAME\n",
    "df = pd.DataFrame(lista)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.head(1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(df.loc[0:5, 0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## SETA COLUNAS\n",
    "df.columns=['url', 'nome', 'preco']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ARRUMA LINK DO PRODUTO\n",
    "tempPosicao,tempCelula = '',''\n",
    "for i in df.index:\n",
    "    tempCelula = df.loc[i, 'url']\n",
    "    tempPosicao = tempCelula.find('href=')\n",
    "    df.loc[i, 'url'] = tempCelula[tempPosicao+7:]\n",
    "#df.loc[0:, 'url'] = df['url'].map(lambda d: \"{}\".format(d[66:]))\n",
    "df.loc[0:, 'url'] = df['url'].map(lambda d: \"{}\".format(\"https://www.americanas.com.br/\" + d ))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(tempPosicao)\n",
    "print(tempCelula)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.loc[15: ,'url']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ARRUMA PREÇO DO PRODUTO\n",
    "df.loc[0:, 'preco'] = df['preco'].map(lambda d: \"{}\".format(d[3:]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## ARRUMA PREÇO\n",
    "tempPosicao,tempCelula = '',''\n",
    "for i in df.index:\n",
    "    tempCelula = df.loc[i, 'preco']\n",
    "    tempPosicao = tempCelula.find(',')\n",
    "    df.loc[i, 'preco'] = tempCelula[0:tempPosicao+3]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(tempCelula)\n",
    "print(tempPosicao)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_csv(str(hoje)+'_523_ecommerce.csv', encoding='iso8859-1', index=False)\n",
    "#df.to_csv(r'Teste.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## GRAVA ARQUIVO EXCEL\n",
    "#with pd.ExcelWriter(str(hoje)+'_523_ecommerce.xlsx') as writer:\n",
    "#    df.to_excel(writer, sheet_name='PrecosAmericanas', engine='openpyxl', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "'''## ORGANIZA OS DADOS EM LISTA\n",
    "lista, lista_temp = [],[]\n",
    "for i in range(len(lista_produtos)):\n",
    "    lista_temp.append(str(lista_produtos[i].a).split('><'))\n",
    "    #print(url[0])\n",
    "    nome = lista_produtos[i].find(class_=tagClassNome).get_text()\n",
    "    #print(nome)\n",
    "    preco = lista_produtos[i].find(class_=tagClassPreco).get_text()\n",
    "    #print(preco)\n",
    "    lista_temp = [url[0], nome, preco]\n",
    "    lista.append(lista_temp)'''"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
