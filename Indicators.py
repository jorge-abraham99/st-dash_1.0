import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from binance import prices
from tasa import Tasa_BCV, reservas_excedentes,liquidity,Paralelo_Telegram
from terminal import FreeTerminal
import seaborn as sns

#rv = reservas_excedentes('https://www.bcv.org.ve/sites/default/files/EstadisticasGeneral/1_1_4.xls')
liq = liquidity('https://www.bcv.org.ve/sites/default/files/indicadores_sector_monetario/liquidez_monetaria_semanal1.xls')
df1 = prices().df

Bloom = FreeTerminal(['ETHUSDT','BTCUSDT'],['EURUSD=X','CL=F','^GSPC','GC=F'])

Paralelo_fecha = Paralelo_Telegram('https://t.me/s/enparalelovzlatelegram').get_prices()["Fecha"][-1]
Paralelo_precio = Paralelo_Telegram('https://t.me/s/enparalelovzlatelegram').get_prices()['Dolar'][-1]
st.set_page_config(
page_title = 'Indicadores en Tiempo Real', page_icon = 'Active',
layout = 'wide')

Tipo_de_orden = st.sidebar.selectbox('Tipo de Operacion', ('SELL', 'BUY'))
Fecha_Liq = st.sidebar.text_input('Fecha de Inicio','01/01/2023')
df1 = df1.loc[df1['Tipo'] == Tipo_de_orden]
liq = liq.get_data(Fecha_Liq)

col1, col2,col3,col4 = st.columns([0.4,0.4,0.1,0.1])
col1.metric("Tasa BCV ", Tasa_BCV('https://www.bcv.org.ve').usd)
col2.metric("Tasa BCV EUR", Tasa_BCV('https://www.bcv.org.ve').eur)
col3.metric(f"Tasa Paralelo: {Paralelo_fecha}", Paralelo_precio)
Spread = float(Paralelo_precio) / float(Tasa_BCV('https://www.bcv.org.ve').usd)
col4.metric("Spread Paralelo/Oficial" ,str(round((Spread - 1) * 100,3)) + '%')


with col1:
    st.markdown("***")
    st.markdown('### Precios Binance')
    st.dataframe(df1,width=550, height=220,hide_index=True)
    st.markdown("### Indicadores Internacionales")
    st.dataframe(Bloom.create_df(),width=550, height=220,hide_index=True)

#fig1, (ax1 , ax2) = plt.subplots(2,1, figsize=(6, 3))
#ax1.plot( 'Semana','LIQUIDEZ', color = 'blue',data = liq)
#ax1.set_title('Liquidez Bancaria - Liquidez Actual: {:,}'.format(round(liq['LIQUIDEZ'][0],2)))
#ax2.plot( 'Semana','VARIACIÓN', color = 'red',data = liq)
#ax2.set_title('Variacion Liquidez Bancaria - Ultima Variacion: {:,}%'.format(round(liq['VARIACIÓN'][0],2)))
#fig1.tight_layout()

sns.set()
fig1, axes = plt.subplots(2,1, figsize=(6, 3))
sns.lineplot(x = 'Semana', y = "LIQUIDEZ", data=liq,ax = axes[0])
sns.lineplot(x = 'Semana', y = "VARIACIÓN", data=liq, ax = axes[1])
axes[0].set_title('Liquidez Bancaria - Liquidez Actual: {:,}'.format(round(liq['LIQUIDEZ'][0],2)))
axes[0].set_ylabel('VED')
axes[1].set_ylabel('%')
axes[1].set_title('Variacion Liquidez Bancaria - Ultima Variacion: {:,}%'.format(round(liq['VARIACIÓN'][0],2)))
fig1.tight_layout()



with col2:
   st.markdown("***")
   st.pyplot(fig1)

