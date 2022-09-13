import requests
import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
import streamlit as st

today = date.today()  #date
yesterday = today - timedelta(days = 1)
daten = {}
for i in range(40):
  d = yesterday - timedelta(days=i)
  if d.weekday() < 5:
    s = d.strftime("%d%b%Y").upper()
    m = d.strftime("%b").upper()
    daten[s] = m
    #print(m)
url1 = []
for s,m in daten.items():
  url = "https://www1.nseindia.com/content/historical/EQUITIES/2022/{}/cm{}{}.zip".format(m,s,"bhav.csv")
  try:
     r = requests.get(url)
     r.status_code()
  except Exception:
   if(r.status_code == 200):
      pass
      url1.append(url)
#print(url1)

st.header("stock dashboard")
st.subheader("nse 7 days")

present_url = url1[0:7]
df = pd.DataFrame()
for k in present_url:
  dff = pd.read_csv(k)
  df = df.append(dff)
mask = df['SERIES'].values == 'EQ'
df = df.loc[mask]
df = df.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
p = df.groupby('SYMBOL')['CLOSE'].mean().rename('Present price MA')
dff = pd.DataFrame(p)
df_pri = dff.dropna()
df_price_present7 = df_pri.groupby('SYMBOL').first()

df = df[(df['TOTTRDQTY'] > 100000)]
v = df.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('present Volume MA')
dff0 = pd.DataFrame(v)
df_vol = dff0.dropna()
df_volume_present7 = df_vol.groupby('SYMBOL').first()


past_url = url1[7:14]
df1 = pd.DataFrame()
for k in past_url:
  dff = pd.read_csv(k)
  df1 = df1.append(dff)
mask = df1['SERIES'].values == 'EQ'
df1 = df1.loc[mask]
df1 = df1.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
t = df1.groupby('SYMBOL')['CLOSE'].mean().rename('past price MA')
dff1 = pd.DataFrame(t)
df_pric = dff1.dropna()
df_price_past7 = df_pric.groupby('SYMBOL').first()

df1 = df1[(df1['TOTTRDQTY'] > 100000)]
s = df1.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('past Volume MA')
df = pd.DataFrame(s)
df_volu = df.dropna()
df_volume_past7 = df_volu.groupby('SYMBOL').first()


df = pd.merge(df_price_past7,df_price_present7,on = 'SYMBOL')
df0 = pd.merge(df_volume_present7, df_volume_past7, on = 'SYMBOL')

volume_ma = (df0['present Volume MA'] - df0['past Volume MA']) / df0['past Volume MA'] *100
volume_ma = pd.DataFrame(volume_ma)
volume_ma.columns = ['volume7']
volume_MA = volume_ma[volume_ma.volume7 > 20]

close_MA = (df['Present price MA'] - df['past price MA']) / df['past price MA'] *100
close_MA = pd.DataFrame(close_MA)
close_MA.columns = ['close_price7']
close_MA = close_MA[close_MA.close_price7 > 20]

df_1 = pd.merge(volume_MA, close_MA, on='SYMBOL', how='inner')
df_1


st.subheader("nse 13 days")

present_url = url1[0:13]
df2 = pd.DataFrame()
for k in present_url:
  dff = pd.read_csv(k)
  df2 = df2.append(dff)
mask = df2['SERIES'].values == 'EQ'
df2 = df2.loc[mask]
df2 = df2.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
p = df2.groupby('SYMBOL')['CLOSE'].mean().rename('Present price MA')
dff3 = pd.DataFrame(p)
df_pri13 = dff3.dropna()
df_price_present13 = df_pri13.groupby('SYMBOL').first()

df2 = df2[(df2['TOTTRDQTY'] > 100000)]
v = df2.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('present Volume MA')
dff4 = pd.DataFrame(v)
df_vol13 = dff4.dropna()
df_volume_present13 = df_vol13.groupby('SYMBOL').first()


past_url = url1[13:26]
df3 = pd.DataFrame()
for k in past_url:
  dff = pd.read_csv(k)
  df3 = df3.append(dff)
mask = df3['SERIES'].values == 'EQ'
df3 = df3.loc[mask]
df3 = df3.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
t = df3.groupby('SYMBOL')['CLOSE'].mean().rename('past price MA')
dff5 = pd.DataFrame(t)
df_pric13 = dff5.dropna()
df_price_past13 = df_pric13.groupby('SYMBOL').first()

df3 = df3[(df3['TOTTRDQTY'] > 100000)]
s = df3.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('past Volume MA')
dff6 = pd.DataFrame(s)
df_volu13 = dff6.dropna()
df_volume_past13 = df_volu13.groupby('SYMBOL').first()


df13p = pd.merge(df_price_past13,df_price_present13,on = 'SYMBOL')
df13v = pd.merge(df_volume_present13, df_volume_past13, on = 'SYMBOL')

volume_ma = (df13v['present Volume MA'] - df13v['past Volume MA']) / df13v['past Volume MA'] *100
volume_ma = pd.DataFrame(volume_ma)
volume_ma.columns = ['volume13']
volume_MA = volume_ma[volume_ma.volume13 > 20]

close_MA = (df13p['Present price MA'] - df13p['past price MA']) / df13p['past price MA'] *100
close_MA = pd.DataFrame(close_MA)
close_MA.columns = ['close_price13']
close_MA = close_MA[close_MA.close_price13 > 20]

df_2 = pd.merge(volume_MA, close_MA, on='SYMBOL', how='inner')
df_2

st.subheader("BSE 7 days")

today = date.today()
yesterday = today - timedelta(days = 1)
daten = []
for i in range(40):
    d = yesterday - timedelta(days=i)
    if d.weekday() < 5:
      s = d.strftime("%d%m%y")
      daten.append(s)
#print(daten)
url2 = []
for i in daten:
  url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}{}{}.ZIP".format(i,"_","CSV")
  hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
  r = requests.get(url, headers= hdr)
  if(r.status_code == 200):
     pass
     url2.append(url)
#print(url2)


present_link = url2[0:7]
df = pd.DataFrame()
for k in present_link:
  hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
  dff = pd.read_csv(k,storage_options=hdr)
  df = df.append(dff)
df = df.loc[df['SC_GROUP'].isin(['X ','XT'])]
df = df.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
a = df.groupby('SC_NAME')['CLOSE'].mean().rename('present close MA')
df_price_present7p = pd.DataFrame(a)

df = df[(df['NO_OF_SHRS'] > 75000)]
b = df.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('Present volume MA')
df_volume_present7v = pd.DataFrame(b)



past_link = url2[7:14]
df01 = pd.DataFrame()
for k in past_link:
  hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
  dff = pd.read_csv(k,storage_options=hdr)
  df01 = df01.append(dff)
df1 = df01.loc[df01['SC_GROUP'].isin(['X ','XT'])]
df1 = df1.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
c = df1.groupby('SC_NAME')['CLOSE'].mean().rename('past close MA')
df_price_past7p = pd.DataFrame(c)

df1 = df1[(df1['NO_OF_SHRS'] > 75000)]
d = df1.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('past volume MA')
df_volume_past7v = pd.DataFrame(d)

df00 = pd.merge(df_price_present7p,df_price_past7p,on = 'SC_NAME')
df01 = pd.merge(df_volume_present7v,df_volume_past7v,on = 'SC_NAME')

volume_MA = (df01['Present volume MA'] - df01['past volume MA']) / df01['past volume MA'] *100
volume_MA = pd.DataFrame(volume_MA)
volume_MA.columns = ['volume7']
volume_MA = volume_MA[volume_MA.volume7 > 20]

close_MA = (df00['present close MA'] - df00['past close MA']) / df00['past close MA'] *100
close_MA = pd.DataFrame(close_MA)
close_MA.columns = ['close_price7']
close_MA = close_MA[close_MA.close_price7 > 20]

df_3 = pd.merge(volume_MA, close_MA, on='SC_NAME', how='inner')
df_3
