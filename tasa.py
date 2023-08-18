from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import re 

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
def finder(list_,item,item2 = 0,item3 = 0):
    if item2 == 0:
        for i in range(len(list_)):
            if list_[i] == item:
                return i 
    else:
        for i in range(len(list_)):
            if list_[i] == item or list_[i] == item2 or list_[i] == item3  :
                return i
class Paralelo_Telegram:
    def __init__(self, url):
        self.r = requests.get(url)
        self.soup =  BeautifulSoup(self.r.content, 'html.parser')
        self.message = self.soup.find_all('div','tgme_widget_message_text js-message_text')
    def get_prices(self):
        a = {'Dolar':[],'Fecha':[]}
        for i in self.message:
            if '🗓' in i.text:
                j = i.text[finder(i.text,'💵'):finder(i.text,'🔻','🔺','🟰')]
                a['Dolar'].append(float(re.sub("\D", "",j))/100)
                k = i.text[finder(i.text,'🗓'):finder(i.text,'🕒')]
                a['Fecha'].append(k[2:])
        return a