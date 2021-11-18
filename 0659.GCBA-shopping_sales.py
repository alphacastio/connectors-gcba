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


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2020/10/AC_CC_AX05.xlsx"
df1 = pd.read_excel(url1)
df1.columns = df1.iloc[2]
df1 = df1.drop(index=1)
df1 = df1.drop(index=2)
df1 = df1.dropna(subset = ['Ropa y accesorios deportivos'])
df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1.drop(df1.columns[[0]], axis=1)
df1.index = pd.date_range(start='1/1/2013', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1.columns = "Índice a valores constantes Base 2013=100 de ventas en shoppings - " + df1.columns


# In[3]:


url2 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/AC_CC_AX02.xlsx"
df2 = pd.read_excel(url2)
df2.columns = df2.iloc[0]
df2.columns = "Ventas totales en shoppings (miles de pesos) - " + df2.columns
df2 = df2.drop(index=0)
df2 = df2.drop(index=1)
df2 = df2.drop(index=2)
#df2 = df2.drop(index=3)
df2 = df2.dropna(subset = ['Ventas totales en shoppings (miles de pesos) - Patio de comidas, alimentos y kioscos'])
df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2.loc[:, df2.columns.notnull()]
df2 = df2.drop(df2.columns[[0]], axis=1)
df2.index = pd.date_range(start='1/1/2007', periods=len(df2), freq = "MS")
df2.index.name = "Date"
del df2["Ventas totales en shoppings (miles de pesos) - Mes"]


# In[4]:


df3 = df1.merge(df2, right_index = True, left_index=True, how = "right")
df3["country"] = "CABA"

alphacast.datasets.dataset(659).upload_data_from_df(df3, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)




