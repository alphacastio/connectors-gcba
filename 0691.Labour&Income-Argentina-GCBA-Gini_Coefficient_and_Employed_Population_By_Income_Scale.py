#!/usr/bin/env python
# coding: utf-8

# In[87]:


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

# In[88]:


#Obtengo la url del file de 'Población ocupada segun escala del ingreso' a través de su xpath
url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=44035'
r = requests.get(url, verify=False)
html = r.content
htmlparser = etree.HTMLParser()
tree = etree.fromstring(html, htmlparser)
xls_address = tree.xpath("//*[@id='post-44035']/div/a/@href")[0]
xls_address


# In[89]:


#Hago el request de la data de Población y genero el dataframe
r = requests.get(xls_address, allow_redirects=True, verify=False)
df = pd.read_excel(r.content, skiprows=1, sheet_name=0)
df = df.dropna(how='all', subset=df.columns[1:])


# In[90]:


df["Periodo"] = df["Periodo"].astype(str)

#Hago un split de 'Periodo' para arreglar la fecha
new = df['Periodo'].str.split(" ", n = 3, expand = True)
df["Trimestre"]= new[0]
df["Trim"]= new[1]
df["Año"]= new[2]

#Reemplazo los trimestres por formato %m-%d
df["Trimestre"] = df["Trimestre"].str.replace("1er." , "-01-01")
df["Trimestre"] = df["Trimestre"].str.replace("2do." , "-04-01")
df["Trimestre"] = df["Trimestre"].str.replace("3er." , "-07-01")
df["Trimestre"] = df["Trimestre"].str.replace("4to." , "-10-01")

#Concateno las columnas para armar 'Date' y dropeo el resto de las col
df['Date'] = df["Año"]+df["Trimestre"]
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

df = df.drop(['Periodo','Trimestre','Trim','Año'], axis=1)

#Agrego el prefijo a las columnas
newCols=[]
for col in df.columns:
    newCols += ['Población ocupada - '+col]        
df.columns = newCols


# In[91]:


#File de Coeficiente de Gini
url2 = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ETOI_I_IOPP_G.xlsx'

#Hago el request de la data y genero el dataframe con su contenido
r2 = requests.get(url2, allow_redirects=True, verify=False)
df2 = pd.read_excel(r2.content, skiprows=1, sheet_name=0)
df2 = df2.dropna(how='all', subset=df2.columns[1:])

df2["Periodo"] = df2["Periodo"].astype(str)

#Hago un split de 'Periodo' para arreglar la fecha
new = df2['Periodo'].str.split(" ", n = 3, expand = True)
df2["Trimestre"]= new[0]
df2["Trim"]= new[1]
df2["Año"]= new[2]

#Reemplazo los trimestres por formato %m-%d
df2["Trimestre"] = df2["Trimestre"].str.replace("1er." , "-01-01")
df2["Trimestre"] = df2["Trimestre"].str.replace("2do." , "-04-01")
df2["Trimestre"] = df2["Trimestre"].str.replace("3er." , "-07-01")
df2["Trimestre"] = df2["Trimestre"].str.replace("4to." , "-10-01")

#Concateno las columnas para armar 'Date'
df2['Date'] = df2["Año"]+df2["Trimestre"]
df2['Date'] = pd.to_datetime(df2['Date'])
df2 = df2.set_index('Date')

df2 = df2.drop(['Periodo','Trimestre','Trim','Año'], axis=1)


# In[92]:


#Mergeo ambos dataframes y le agrego el entity
dfFinal = df.merge(df2, how='outer', left_index=True, right_index=True)
dfFinal['country'] = 'CABA'

alphacast.datasets.dataset(7471).upload_data_from_df(dfFinal, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

