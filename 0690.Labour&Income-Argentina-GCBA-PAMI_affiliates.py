#!/usr/bin/env python
# coding: utf-8

# In[39]:


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

# In[40]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/SS_IN_AX01.xlsx'
df = pd.read_excel(url, sheet_name = 0, skiprows = 2)

df = df.dropna(how = 'all').dropna(how = 'all', subset = df.columns[1:])
df = df.dropna(how='any')
df = df.rename(columns={'Año':'Year',
                        'Población afiliada 1':'Población afiliada - Absoluto',
                        'Unnamed: 3':'Población afiliada - %'})


# In[41]:


df['Month'] = 1
df['Day'] = 1
df['Date'] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")


# In[42]:


df = df[['Date','Población afiliada - Absoluto','Población afiliada - %']]
df = df.set_index('Date')


# In[43]:


df['country']= 'GCBA'

alphacast.datasets.dataset(7459).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

