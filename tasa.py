from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

class Tasa_BCV:
    def __init__(self, url):
        self.r = requests.get(url)
        self.soup =  BeautifulSoup(self.r.text)
        self.usd = self.soup.find("div", "view-tipo-de-cambio-oficial-del-bcv").find(id = 'dolar').find('strong').text.strip().replace(",", ".")
        self.eur = self.soup.find("div", "view-tipo-de-cambio-oficial-del-bcv").find(id = 'euro').find('strong').text.strip().replace(",", ".")

class reservas_excedentes:
    def __init__(self, url):
        self.url = url
        self.df = pd.read_excel(self.url).dropna()
        self.dia = str(self.df['BANCO CENTRAL DE VENEZUELA'][6])[:10]
        self.reserva = self.df['Unnamed: 1'][6]

def create_datetime(i):
    try:
         a = datetime.strptime(i, '%d/%m/%Y')
    except ValueError:
        a = datetime.strptime(i, '%Y/%m/%d')
    return a

class liquidity:
    def __init__(self, url):
        self.url = url
        self.df = pd.read_excel(url , skiprows=[0,1,2,3,5,6]).dropna(axis = 0)
        self.df['Semana'] = self.df['Semana'].astype(str).apply(lambda x: x[:10])
        self.df['Semana'] = self.df['Semana'].apply(lambda x: x.replace('-','/'))
        self.df['Semana'] = self.df['Semana'].apply(create_datetime)
    def get_data(self,fecha):
        self.fecha = fecha
        return self.df.loc[self.df['Semana'] > create_datetime(fecha)]
   
class Tasa_Paralelo:
    def __init__(self, url):
        self.r = requests.get(url)
        self.soup =  BeautifulSoup(self.r.content, 'html.parser')
        self.prom = self.soup.find_all(id="promedios")
        self.usd = self.prom[0].find_all('p')[2].text.strip()[5:].replace(',','.')

class Paralelo_Telegram:
    def __init__(self, url):
        self.r = requests.get(url)
        self.soup =  BeautifulSoup(self.r.content, 'html.parser')
        self.message = self.soup.find_all('div','tgme_widget_message_text js-message_text')
    def get_prices(self):
        a = []
        for i in self.message:
            if '🗓' in i.text:
                a.append(i.text)
        b = []
        for i in a:
            if len(i) < 48:
                b.append({'Fecha':i[2:10],'Hora':i[14:18],'Precio':i[27:32].replace(',','.') })
            else:
                b.append({'Fecha':i[2:10],'Hora':i[14:19],'Precio':i[28:33].replace(',','.') })
        return b