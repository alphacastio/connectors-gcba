#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

# In[4]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/Eoh_03a_0811.xlsx"
df1 = pd.read_excel(url1)
#df1[:2] = df1[:2].ffill(1)
df1.columns =   "Tarifa Promedio - " + df1.iloc[2]
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
df1 = df1.drop(index=2)
df1 = df1.dropna(subset = [df1.columns[3]])
#df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='1/1/2008', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"] = "CABA"

alphacast.datasets.dataset(7434).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




