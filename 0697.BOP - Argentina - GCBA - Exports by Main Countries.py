#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import io

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[14]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=69475'
page = requests.get(url).text


# In[15]:


soup = BeautifulSoup(page, 'html.parser')


# In[16]:


links = soup.find_all('a')
for link in links:
    if 'xlsx' in link.get('href'):
        link_xls = link.get('href')


# In[17]:


xls_file = requests.get(link_xls).content


# In[18]:


#Guardo en una lista todos los nombres de las hojas
sheet_list = pd.ExcelFile(io.BytesIO(xls_file), engine='openpyxl').sheet_names
#Excluyo las hojas que no corresponden a los años
sheet_list = [sheet for sheet in sheet_list if sheet !='AX_CX_PAI' and sheet !='Ficha Técnica']
#Reordeno la lista
sheet_list.reverse()


# In[19]:


#Itero por los nombres de las hojas
for indice, sheet in enumerate(sheet_list):
    df_temp = pd.read_excel(io.BytesIO(xls_file), sheet_name=sheet, engine='openpyxl', skiprows=1)
    #Elimino los espacios de las columnas
    df_temp.columns = df_temp.columns.str.strip()
    df_temp.iloc[0, 1] = df_temp.iloc[0, 0]
    df_temp.iloc[1, 1] = df_temp.iloc[1, 0]
    
#     df_temp.drop('Orden', axis=1, inplace=True)

    for column in df_temp.columns[1:]:
        if df_temp[column].dtype == 'O':
            df_temp[column] = df_temp[column].str.strip()

    df_temp.dropna(subset=['Mercados'], inplace=True)
    df_temp['Date'] = sheet[-4:]
    df_temp['Date'] = pd.to_datetime(df_temp['Date'], format='%Y')
    df_temp.set_index('Date', inplace=True)
    
    if indice==0:
        df = df_temp.copy()
    else:
        df = df.append(df_temp)


# In[20]:


df['country'] = 'CABA'
df = df[['Orden', 'Mercados', 'Millones de dólares', 'country']]

alphacast.datasets.dataset(7525).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

