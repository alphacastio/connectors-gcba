#!/usr/bin/env python
# coding: utf-8

# In[77]:


import pandas as pd
import numpy as np
import requests

from datetime import datetime
from urllib.request import urlopen
from lxml import etree
import io
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[78]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=113254'
r = requests.get(url, verify=False)
html = r.content
htmlparser = etree.HTMLParser()
tree = etree.fromstring(html, htmlparser)
xls_address = tree.xpath("//*[@id='post-113254']/div/a/@href")[0]
xls_address


# In[79]:


#Hago el request de la data y genero el dataframe con su contenido
r = requests.get(xls_address, allow_redirects=True, verify=False)
df = pd.read_excel(r.content, skiprows=2, sheet_name=0, header = [0,1])


# In[80]:


#Concateno los nombres de las columnas
df.columns = df.columns.map(' - '.join)


# In[81]:


df["Año - Unnamed: 0_level_1"] = df["Año - Unnamed: 0_level_1"].astype(str)
#Reemplazo los trimestres por formato %m-%d
df["Año - Unnamed: 0_level_1"] = df["Año - Unnamed: 0_level_1"].str.replace("1er. trimestre" , "-01-01")
df["Año - Unnamed: 0_level_1"] = df["Año - Unnamed: 0_level_1"].str.replace("2do. trimestre" , "-04-01")
df["Año - Unnamed: 0_level_1"] = df["Año - Unnamed: 0_level_1"].str.replace("3er. trimestre" , "-07-01")
df["Año - Unnamed: 0_level_1"] = df["Año - Unnamed: 0_level_1"].str.replace("4to. trimestre" , "-10-01")


# In[82]:


#Creo columnas separadas con el año, mes y dia para luego concatenarlas
df["year"] = df["Año - Unnamed: 0_level_1"].str.split("-", expand = True)[0].replace('',np.nan).fillna(method="ffill")
df["month"] = df["Año - Unnamed: 0_level_1"].str.split("-", expand = True)[1]
df["day"] = df["Año - Unnamed: 0_level_1"].str.split("-", expand = True)[2]


# In[83]:


#Armo la col de Date y elimino las auxiliares y la original
df["Date"] = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
df = df[df["Date"].notnull()]

del df["Año - Unnamed: 0_level_1"]
del df["day"]
del df["month"]
del df["year"]

df = df.set_index("Date")
df.columns = ['Total centrales','Central Térmica de vapor','Central Ciclo Combinado']
df['country'] = 'CABA'


alphacast.datasets.dataset(7449).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

