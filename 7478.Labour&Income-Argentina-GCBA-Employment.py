#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests

from datetime import datetime
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


#Distribución porcentual del empleo privado formal por sexo
url = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/06/EEF_EE_OI_EPF_A512.xlsx'

r = requests.get(url, allow_redirects=True, verify=False)
df = pd.read_excel(r.content, skiprows=1, sheet_name=0)

#Elimino filas con vacíos
df = df.dropna(how='all', subset=df.columns[1:])

#Armo el indice con la fecha
df.index = pd.date_range(start='8/1/2006', periods=len(df), freq = "MS")
df.index.name = "Date"
del df['Período']

#Agrego el prefijo a las columnas
newCols=[]
for col in df.columns:
    newCols += ['Empleo privado - '+col]        
df.columns = newCols


# In[3]:


#Distribución porcentual mensual del empleo privado formal por sexo y calificación ocupacional
url1 = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/06/EEF_EE_OI_EPF_A612.xlsx'

r1 = requests.get(url1, allow_redirects=True, verify=False)
df1 = pd.read_excel(r1.content, skiprows=1, sheet_name=0, header = [0,1])

#Elimino filas con vacíos
df1 = df1.dropna(how='all', subset=df1.columns[1:])

#Concateno los nombres de las columnas
df1.columns = df1.columns.map(' - '.join)

#Armo el indice con la fecha
df1.index = pd.date_range(start='8/1/2006', periods=len(df1), freq = "MS")
df1.index.name = "Date"
del df1['Período - Unnamed: 0_level_1']


# In[4]:


url2 = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/EEF_EE_OI_EPF_A312.xlsx'

r2 = requests.get(url2, allow_redirects=True, verify=False)
df2 = pd.read_excel(r2.content, skiprows=1, sheet_name=0)

#Elimino filas con vacíos
df2 = df2.dropna(how='all', subset=df2.columns[1:])

#Traspongo el df
df2 = df2.rename(columns={'Rama de actividad':'Date'})
df2 = df2.set_index('Date')
df2 = df2.T.reset_index()

#Armo el indice con la fecha
df2.index = pd.date_range(start='5/1/2000', periods=len(df2), freq = "MS")

df2 = df2.rename(columns={df2.columns[1]: "Drop"})
df2 = df2.drop(['index','Drop'], axis=1)


# In[5]:


# Empleo privado formal por tamaño de la empresa
url3 = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/EEF_EE_OI_EPF_A212.xlsx'

r3 = requests.get(url3, allow_redirects=True, verify=False)
df3 = pd.read_excel(r3.content, skiprows=1, sheet_name=0)

#Elimino filas con vacíos
df3 = df3.dropna(how='all', subset=df3.columns[1:])
df3 = df3.dropna(how='any')

#Elimino las columnas con variaciones %
df3 = df3.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 5','Unnamed: 6','Unnamed: 8','Unnamed: 9'], axis=1)

#Armo el indice con la fecha
df3.index = pd.date_range(start='5/1/2000', periods=len(df3), freq = "MS")
df3.index.name = "Date"
del df3['Período']

#Agrego el prefijo 
newCols=[]
for col in df3.columns:
    newCols += ['Tamaño de la empresa - '+col]        
df3.columns = newCols


# In[6]:


#Mergeo todos los dataframes en uno solo
dfFinal = df3.merge(df2, how='outer', left_index=True, right_index=True).merge(df1, how='outer', left_index=True, right_index=True).merge(df, how='outer', left_index=True, right_index=True)

dfFinal


# In[9]:


for col in dfFinal.columns:
    dfFinal[col] = pd.to_numeric(dfFinal[col], errors="coerce")


# In[10]:


dfFinal['country'] = 'CABA'

alphacast.datasets.dataset(7478).upload_data_from_df(dfFinal, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




