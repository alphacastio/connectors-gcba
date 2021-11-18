#!/usr/bin/env python
# coding: utf-8

# In[27]:


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

# In[28]:


url = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/PGB_ITAE_b12.xlsx"
df = pd.read_excel(url)
df = df.iloc[1:]
names = ["Indicador Trimestral de Actividad Económica - Base promedio 2012 = 100"]
data = [df["Unnamed: 1"].dropna()]
df = pd.concat(data, axis=1, keys=names)
df.index = pd.date_range(start='1/1/2013', periods=len(df), freq = "Q")
df.index.name = "Date"


# In[30]:


df["country"] = "CABA"

alphacast.datasets.dataset(655).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)
