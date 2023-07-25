import pandas as pd
import numpy as np
import requests
import json


def get_data(methods,compra_venta):
    j = 1
    i = 1
    pandas = []
    while j > 0:
  
        headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    
        data = {
    "asset": "USDT",
    "fiat": "VES",
    "merchantCheck": True,
    "page": i,
    "payTypes": methods,
    "rows": 20,
    "tradeType": compra_venta}
        
        i += 1
        r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
        pandas.append(pd.DataFrame([r.json()['data'][i]['adv'] for i in range(len( r.json()['data']))]))
        j = r.json()['total']
    df = pd.concat(pandas)
    df = df[['advNo', 'classify', 'tradeType', 'asset', 'fiatUnit','price', 'initAmount', 'surplusAmount',
       'maxSingleTransAmount', 'minSingleTransAmount','payTimeLimit', 'tradeMethods','assetScale', 'fiatScale','priceScale', 'fiatSymbol', 'isTradable', 'dynamicMaxSingleTransAmount',
       'minSingleTransQuantity', 'maxSingleTransQuantity',
       'dynamicMaxSingleTransQuantity', 'tradableQuantity', 'commissionRate']]
    df = df.loc[ df['classify'] == 'profession']
    df[['price', 'initAmount', 'surplusAmount', 'maxSingleTransAmount', 'minSingleTransAmount','payTimeLimit','assetScale', 'fiatScale','priceScale', 'dynamicMaxSingleTransAmount','minSingleTransQuantity', 'maxSingleTransQuantity',
       'dynamicMaxSingleTransQuantity', 'tradableQuantity', 'commissionRate']] = df[['price', 'initAmount', 'surplusAmount', 'maxSingleTransAmount', 'minSingleTransAmount','payTimeLimit','assetScale', 'fiatScale','priceScale', 'dynamicMaxSingleTransAmount','minSingleTransQuantity', 'maxSingleTransQuantity',
       'dynamicMaxSingleTransQuantity', 'tradableQuantity', 'commissionRate']].astype(float)
    return df

class prices:
    def __init__(self):
        self.Methods = [['BankVenezuela','BancoDeVenezuela'],['Mercantil'],['Banesco'],['Provincial'],['Bancamiga']]
        self.Nombres = [ 'BDV', 'Mercantil','Banesco','Provincial','Bancamiga']
        self.dfs = []
        for i in range(len( self.Methods )):
            k = get_data(self.Methods[i],'BUY')
            j = pd.DataFrame(data = {'Banco': [self.Nombres[i]] ,'Tipo':['BUY'],'USDT Disponible': [k['tradableQuantity'].astype(float).sum()],
                                     'Precio': [k['price'].astype('float').mean()],'Precio Max':[k['price'].astype('float').max()],'Precio Min':[k['price'].astype('float').min()] })
            self.dfs.append(j)
        for i in range(len( self.Methods )):
            k = get_data(self.Methods[i],'SELL')
            j = pd.DataFrame(data = {'Banco': [self.Nombres[i]] ,'Tipo':['SELL'],'USDT Disponible': [k['tradableQuantity'].astype(float).sum()],
                                     'Precio': [k['price'].astype('float').mean()],'Precio Max':[k['price'].astype('float').max()],'Precio Min':[k['price'].astype('float').min()]})
            self.dfs.append(j)
        self.df = pd.concat(self.dfs)
