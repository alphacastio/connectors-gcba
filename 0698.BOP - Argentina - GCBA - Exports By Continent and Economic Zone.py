#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import io

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=24610'
page = requests.get(url).text


# In[3]:


soup = BeautifulSoup(page, 'html.parser')


# In[4]:


links = soup.find_all('a')
for link in links:
    if 'xlsx' in link.get('href'):
        link_xls = link.get('href')


# In[5]:


xls_file = requests.get(link_xls).content

df = pd.read_excel(xls_file, sheet_name=0, engine='openpyxl', skiprows=1)
#Se eliminan todas las filas que no tienen valores en los totales
df.dropna(subset=[df.columns[1]], inplace=True)


# In[6]:


#Se setea el indice y se transpone, asi las fechas quedan como indice
df.set_index(df.columns[0], inplace=True)
df = df.T


# In[7]:


#Se renombra el indice y el eje
df.index.name='Date'
df.rename_axis(None, axis=1, inplace=True)
df.index = df.index.astype(str).str.replace('\*$', '', regex=True)


# In[8]:


#Se cambia el formato del indice a fecha
df.index = pd.to_datetime(df.index, format='%Y')
df['country'] = 'CABA'

alphacast.datasets.dataset(7550).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


