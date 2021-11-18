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


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_consumo_de_energia.xlsx"
df1 = pd.read_excel(url1)
df1[:1] = df1[:1].ffill(1)
df1.columns =  df1.iloc[0] + " - " + df1.iloc[1]
df1 = df1.drop(index=0)
df1 = df1.drop(index=1)
#df1 = df1.drop(index=0)
df1 = df1.dropna(subset = [df1.columns[10]])
#df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
#df1 = df1[df1.columns.drop(list(df1.filter(regex='Participación')))]
df1["country"] = "CABA"


# In[3]:


url2= "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_uso_energetico.xlsx"
df2 = pd.read_excel(url2)
df2[:1] = df2[:1].ffill(1)
df2.columns =  df2.iloc[0] + " - " + df2.iloc[1]
df2 = df2.drop(index=0)
df2 = df2.drop(index=1)
#df2 = df2.drop(index=0)
df2 = df2.dropna(subset = [df2.columns[10]])
#df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2[df2.columns.dropna()]
df2.index = pd.date_range(start='10/1/2001', periods=len(df2), freq = "MS")
df2.index.name = "Date"
#df2 = df2[df2.columns.drop(list(df2.filter(regex='Participación')))]
df2["country"] = "CABA"


# In[4]:


alphacast.datasets.dataset(667).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

alphacast.datasets.dataset(669).upload_data_from_df(df2,
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


