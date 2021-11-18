#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import datetime
import io

import numpy as np
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2020/10/AC_S_AX05.xlsx"
df1 = pd.read_excel(url1)
df1.columns = df1.iloc[1]
df1 = df1.drop(index=1)
df1 = df1.dropna(subset = ['Bebidas'])
df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1.drop(df1.columns[[0]], axis=1)
df1.index = pd.date_range(start='1/1/2013', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1.columns = "Índice a valores constantes Base 2013=100 de ventas en supermercados - " + df1.columns
df1


# In[3]:


url2 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/AC_S_AX04.xlsx"
df2 = pd.read_excel(url2)
df2.columns = df2.iloc[0]
df2.columns = "Ventas totales en supermercados (miles de pesos) - " + df2.columns
df2 = df2.drop(index=0)
df2 = df2.drop(index=1)
df2 = df2.drop(index=2)
df2 = df2.dropna(subset = ['Ventas totales en supermercados (miles de pesos) - Bebidas'])
df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2.drop(df2.columns[[0, 1]], axis=1)
df2.index = pd.date_range(start='1/1/2007', periods=len(df2), freq = "MS")
df2.index.name = "Date"
df2 = df2.rename(columns={np.nan: "Ventas totales en supermercados (miles de pesos) - Otros"}) 


# In[4]:


url3 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/AC_S_AX02.xlsx"
df3 = pd.read_excel(url3)
df3.columns = df3.iloc[1]
#df3.columns = "Ventas totales en supermercados (miles de pesos) - " + df3.columns
df3 = df3.drop(index=0)
df3 = df3.drop(index=1)
#df3 = df3.drop(index=2)
df3 = df3.dropna(subset = ['Operaciones'])
df3 = df3[~df3.iloc[:, 0].astype(str).str.isdigit()]
df3 = df3.drop(df3.columns[[0, 1]], axis=1)
df3.index = pd.date_range(start='1/1/2007', periods=len(df3), freq = "MS")
df3.index.name = "Date"
#df3 = df3.rename(columns={np.nan: "Ventas totales en supermercados (miles de pesos) - Otros"}) 
df3


# In[5]:


df4 = df1.merge(df2, right_index = True, left_index=True, how = "right").merge(df3, right_index = True, left_index=True)


# In[6]:


for col in df4.columns:
    df4[col] = pd.to_numeric(df4[col], errors="coerce")


# In[7]:


df4["country"] = "CABA"

alphacast.datasets.dataset(657).upload_data_from_df(df4, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)



