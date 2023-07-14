import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from binance import prices
from tasa import Tasa_BCV, reservas_excedentes,liquidity

#rv = reservas_excedentes('https://www.bcv.org.ve/sites/default/files/EstadisticasGeneral/1_1_4.xls')
liq = liquidity('https://www.bcv.org.ve/sites/default/files/indicadores_sector_monetario/liquidez_monetaria_semanal1.xls').df
df1 = prices().df
st.set_page_config(
page_title = 'Indicadores en Tiempo Real', page_icon = 'Active',
layout = 'wide')

Tipo_de_orden = st.sidebar.selectbox('Tipo de Operacion', ('SELL', 'BUY'))
col1, col2, col3 = st.columns(3)
col1.metric("Tasa BCV ", Tasa_BCV('https://www.bcv.org.ve').usd)
col2.metric("Tasa BCV EUR", Tasa_BCV('https://www.bcv.org.ve').eur)
#col3.metric("Excedente " + rv.dia ,rv.reserva )

st.markdown('### Precios Binance')

st.dataframe(df1.loc[df1['Tipo'] == Tipo_de_orden])



