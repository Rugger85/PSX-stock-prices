import streamlit as st
from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import numpy as np
import re

#st.image("black-and-green-modern-material-header-with-a-hexagonal-mesh-design-banner-with-polygonal-grid-and-blank-space-for-your-logo-abstract-website-design-vector.jpg")

st.title("Welcome to PSX data")
st.markdown=("---")
url = urllib.request.urlopen("https://dps.psx.com.pk/screener")
live_web = bs(url, 'html.parser')

data = live_web.find_all('tr')

stocks = re.findall(r'<td data-order="([^"]+)">', str(data))

lists = []

for stock in stocks:
    stock_row = live_web.find('td', {'data-order':stock})
    columns = stock_row.find_next_siblings('td', limit=10)
    price = columns[3]
    price_value = price.text.strip()
    mc = columns[2]
    market_cap = mc.text.strip()
    volume = columns[9]
    volume_30days = volume.text.strip()
    lists.append([stock, price_value, volume_30days, market_cap])


df = pd.DataFrame(lists, columns=['Stock symbol', 'Price', 'Vol 30 days', 'Market Cap'])

st.dataframe(df, width=1200)

st.markdown=("___")

select = st.selectbox("Stock symbol?", options=stocks)
# st.header(select,)
print(select)
selected = df.loc[df['Stock symbol']==select]

stock_row1 = live_web.find('td', {'data-order':select})
columns1 = stock_row1.find_next_siblings('td', limit=10)
change = columns1[4]
x = change.text.strip()
y = re.findall(r"[-]?\d+\.\d+",x)
l = float(y[0])

st.metric(label=select, value=float(selected['Price']), delta=l)

st.markdown=("---")

st.dataframe(selected, width=1200)

#st.image("images.jpeg", width=700)
