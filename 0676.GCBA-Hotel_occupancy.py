#!/usr/bin/env python
# coding: utf-8

# In[5]:


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

# In[6]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/Eoh_04_0811.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   "Ocupación de plazas - " + df1.iloc[1] + " - " + df1.iloc[2]
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
df1 = df1.drop(index=2)
df1 = df1.dropna(subset = [df1.columns[3]])
#df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='1/1/2008', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"] = "CABA"
df1 = df1.replace("///", np.nan).replace("-", np.nan)


# In[7]:


url2 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2019/05/Eoh_02a_0811.xlsx"
df2 = pd.read_excel(url2)
df2[:2] = df2[:2].ffill(1)
df2.columns =   "Ocupación de habitaciones - " + df2.iloc[1] + " - " + df2.iloc[2]
df2 = df2.drop(index=1)
df2 = df2.drop(index=0)
df2 = df2.drop(index=2)
df2 = df2.dropna(subset = [df2.columns[3]])
#df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2[df2.columns.dropna()]
df2.index = pd.date_range(start='1/1/2008', periods=len(df2), freq = "MS")
df2.index.name = "Date"
df2=df2.replace("///", np.nan).replace("-", np.nan)


df3 = df1.merge(df2, right_index=True, left_index=True)

alphacast.datasets.dataset(676).upload_data_from_df(df3, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

