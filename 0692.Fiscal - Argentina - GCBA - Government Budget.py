#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


page = requests.get('https://www.estadisticaciudad.gob.ar/eyc/?p=29115')
soup = BeautifulSoup(page.content, 'html.parser')


# In[3]:


for link in soup.find_all('a'):
    if 'Ver Archivo' in link.get_text():
        link_xls = link.get('href')


# In[4]:


df = pd.read_excel(link_xls, engine='openpyxl', skiprows=1)


# In[5]:


#Hago que las filas que comiencen con Nota: y Fuente: sean NaN
df['Concepto'] = df['Concepto'].replace('^Nota: ', np.nan, regex=True).replace('^Fuente: ', np.nan, regex=True)
#Elimino los espacios al inicio de los nombres
df['Concepto'] = df['Concepto'].str.strip()


# In[6]:


#Elimino las filas con todos NaN
df.dropna(how='all', axis=0, inplace=True)


# In[7]:


#Creo una columna para anidar los nombres
df['Nivel'] = np.nan
#Para los casos que comiencen con digitos seguidos de un parentesis ("1)"), copie el valor de la columna Concepto
df['Nivel'] = np.where((df.Concepto.str.contains('^\d\)')) | (df.Concepto.str.contains('^\d{2}\)')), 
                                                             df['Concepto'], df['Nivel'])

#Completa los NaN a partir de los valores de filas anteriores
df['Nivel'].fillna(method='ffill', inplace=True)

#Concatena los niveles
df['Nivel'] = np.where(df['Nivel'] != df['Concepto'], df['Nivel'] + ' - ' + df['Concepto'], df['Nivel'])


# In[8]:


#Remueve la numeracion (al principio de cada fila) de los subniveles para que no sea confusa la notación
df['Nivel'] = np.where(df['Nivel'] != df['Concepto'], df['Nivel'].replace('^\d\)', '', regex=True), df['Nivel'])
df['Nivel'] = np.where(df['Nivel'] != df['Concepto'], df['Nivel'].replace('^\d{2}\)', '', regex=True), df['Nivel'])
#Elimino los espacios
df['Nivel'] = df['Nivel'].str.strip()


# In[9]:


#Elimino la columna Concepto
df.drop('Concepto', axis=1, inplace=True)

#Seteo el índice y traspongo
df.set_index('Nivel', inplace=True)
df = df.T


# In[10]:


#Para que pueda hacer el reemplazo del asterisco se convierte a string y luego se hace el reemplazo, sino genera nan
df.index = df.index.astype(str).str.replace('\*$', '', regex=True)
#Cambio el formato a fecha
df.index = pd.to_datetime(df.index, format='%Y', errors='coerce')

#Renombro el axis
df.rename_axis(None, axis=1, inplace=True)
#Renombro el indice
df.index.rename('Date', inplace=True)

df['country'] = 'CABA'


alphacast.datasets.dataset(7475).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

