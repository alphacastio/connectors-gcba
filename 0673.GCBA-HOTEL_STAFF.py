#!/usr/bin/env python
# coding: utf-8

# In[9]:


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

# In[10]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2020/11/Eoh_PnoA_0811.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   "Personal No Asalariado - " + df1.iloc[1] + " - " + df1.iloc[2]
df1 = df1.drop(df1.columns[[1]], axis = 1)
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
df1 = df1.drop(index=2)
df1 = df1.dropna(subset = [df1.columns[3]])
#df1 = df1.iloc[2: , 3:-2]
#df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='1/1/2008', periods=len(df1), freq = "QS")
df1.index.name = "Date"
#df1 = df1[df1.columns.drop(list(df1.filter(regex='Participación')))]
df1


# In[11]:


url2 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/Eoh_PA_0811.xlsx"
df2 = pd.read_excel(url2)
df2[:2] = df2[:2].ffill(1)
df2.columns =  "Personal Asalariado - " + df2.iloc[1] + " - " + df2.iloc[2]
df2 = df2.drop(df2.columns[[1]], axis = 1)
df2 = df2.drop(index=1)
df2 = df2.drop(index=0)
df2 = df2.drop(index=2)
df2 = df2.dropna(subset = [df2.columns[3]])
#df2 = df2.iloc[2: , 3:-2]
#df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2[df2.columns.dropna()]
df2.index = pd.date_range(start='1/1/2008', periods=len(df2), freq = "QS")
df2.index.name = "Date"


df3 = df1.merge(df2, right_index=True, left_index=True)

alphacast.datasets.dataset(7432).upload_data_from_df(df3, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


