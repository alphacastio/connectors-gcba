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


url = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/Indice_convenios.xlsx"
df = pd.read_excel(url)


# In[3]:


df = df[0:8].T
df.columns = df.iloc[0]
df = df.iloc[1:]
df = df.replace("sep-21*", "2021-09-01")
df = df.replace("ago-21*", "2021-08-01")
df.index = pd.to_datetime(df["Índice1"])
del df["Índice1"]
df.index.name = "Date"
df["country"] = "CABA"


alphacast.datasets.dataset(654).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


