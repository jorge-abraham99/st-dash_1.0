import requests
import yfinance as yf
import pandas as pd

class FreeTerminal():
    def __init__(self,crypto,ticker):
        self.prices = []
        self.names = []
        self.crypto = crypto
        self.ticker = ticker
        for i in range(len(self.crypto)):
            c = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={self.crypto[i]}").json()['price']
            c = float(c)
            self.names.append(self.crypto[i])
            self.prices.append(c) 
        for i in range(len(self.ticker)):
            d = yf.Ticker(self.ticker[i]).info
            e = (d['bid'] + d['ask'])/2
            self.names.append(d['shortName'])
            self.prices.append(e)
    def create_df(self):
        return pd.DataFrame({'Indicadores': self.names,'Precios': self.prices})