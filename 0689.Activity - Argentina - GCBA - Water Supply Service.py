#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)



page = requests.get('https://www.estadisticaciudad.gob.ar/eyc/?p=68652')


# In[3]:


soup = BeautifulSoup(page.content, 'html.parser')

for link in soup.find_all('a'):
    if 'Ver Archivo' in link.get_text():
        link_xls= link.get('href')


# In[4]:


df = pd.read_excel(link_xls, engine='openpyxl', skiprows=2)


# In[5]:


df.rename(columns={'Año':'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')

df.dropna(subset=['Date'], inplace=True)


# In[6]:


df.set_index('Date', inplace=True)
df['country'] = 'CABA'

alphacast.datasets.dataset(7453).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

