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


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2020/06/Eoh_VA_0811.xlsx"
df1 = pd.read_excel(url1)
df1[:1] = df1[:1].ffill(1)
df1.columns =   "Viajeros Hospedados - " + df1.iloc[1]
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
df1 = df1.dropna(subset = [df1.columns[3]])
#df1 = df1.iloc[2: , 3:-2]
#df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='1/1/2013', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"] = "CABA"


# In[4]:


for col in df1.columns:
    df1[col] = pd.to_numeric(df1[col], errors="coerce")

df1["country"] = "CABA"

alphacast.datasets.dataset(7433).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


