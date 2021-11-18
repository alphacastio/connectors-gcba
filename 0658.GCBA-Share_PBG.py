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


url = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/AX_CX_TOT.xlsx"
df = pd.read_excel(url)
df = df.iloc[2:]
names = ["Participación en PGB (%)"]
data = [df["Unnamed: 2"].dropna()]
df = pd.concat(data, axis=1, keys=names)
df.index = pd.date_range(start='1/1/1993', periods=len(df), freq = "YS")
df.index.name = "Date"
df


# In[3]:


for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# In[4]:


df["country"] = "CABA"

alphacast.datasets.dataset(658).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)




