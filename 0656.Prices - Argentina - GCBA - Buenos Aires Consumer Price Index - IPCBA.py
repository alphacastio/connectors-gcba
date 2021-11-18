#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
from alphacast import Alphacast
from dotenv import dotenv_values


# In[2]:


#IPCBA. Evolución del Nivel General, de los bienes y de los servicios
link_xls = []
page_1 = requests.get('https://www.estadisticaciudad.gob.ar/eyc/?p=27386')
soup_1 = BeautifulSoup(page_1.content, 'html.parser')

for link in soup_1.find_all('a'):
    if 'xlsx' in link.get('href'):
        link_xls.append(link.get('href'))


# In[3]:


#IPCBA. Evolución del nivel general, estacionales, regulados y resto IPCBA.
page_2 = requests.get('https://www.estadisticaciudad.gob.ar/eyc/?p=50914')
soup_2 = BeautifulSoup(page_2.content, 'html.parser')

for link in soup_2.find_all('a'):
    if 'xlsx' in link.get('href'):
        link_xls.append(link.get('href'))


# In[4]:


df1 = pd.read_excel(link_xls[0], skiprows=3)
#Eliminamos filas sin datos y renombramos la primera columna (fecha)
df1.dropna(subset = ['Nivel General'], inplace=True)
df1.rename(columns={df1.columns[0]:'Date'}, inplace=True)

#Reemplazamos el asterisco en el ultimo mes y pasamos a formato fecha
df1['Date'] = df1['Date'].replace('\*', '', regex=True)

dict_months = {"ene": "01-01", "feb": "02-01","mar": "03-01","abr": "04-01", "may": "05-01",
               "jun": "06-01","jul": "07-01","ago": "08-01", "sep": "09-01", "oct": "10-01", 
               "nov": "11-01","dic": "12-01"}

df1['Date'] = df1['Date'].replace(dict_months, regex=True)
df1['Date'] = pd.to_datetime(df1['Date'])
df1.set_index('Date', inplace=True)
#Solo se mantienen unas columnas
df1 = df1[['Nivel General', 'Bienes', 'Servicios']]
df1 = df1.add_prefix('Evolución del IPCBA - ')


# In[5]:


df2 = pd.read_excel(link_xls[1], skiprows=3)
df2.dropna(subset = ['Estacionales'], inplace=True)
df2.rename(columns={df2.columns[0]:'Date'}, inplace=True)

df2['Date'] = df2['Date'].replace('\*', '', regex=True)

df2['Date'] = df2['Date'].replace(dict_months, regex=True)
df2['Date'] = pd.to_datetime(df2['Date'])
df2.set_index('Date', inplace=True)
df2 = df2[['Estacionales', 'Regulados']]
df2 = df2.add_prefix('Evolución del IPCBA - ')


# In[6]:


df = df1.merge(df2, right_index = True, left_index=True)
df['country'] = 'CABA'


# In[7]:


API_KEY = dotenv_values(".env").get("ALPHACAST_API_KEY")

alphacast = Alphacast(API_KEY)


# In[8]:


#Cargo la data a Alphacast
alphacast.datasets.dataset(656).upload_data_from_df(df, 
                 deleteMissingFromDB = False, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




