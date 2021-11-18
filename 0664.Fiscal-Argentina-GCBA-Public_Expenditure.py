#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests

from datetime import datetime
from urllib.request import urlopen
from lxml import etree
import io
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=29116'
r = requests.get(url, verify=False)
html = r.content
htmlparser = etree.HTMLParser()
tree = etree.fromstring(html, htmlparser)
xls_address = tree.xpath("//*[@id='post-29116']/div/a/@href")[0]


# In[3]:


r = requests.get(xls_address, allow_redirects=True, verify=False)
df = pd.read_excel(r.content, skiprows=1, sheet_name=0)


# In[4]:


df = df.dropna(how='all', subset = df.columns[1:])
df = df.set_index('Finalidad')
df = df.T.reset_index()
df = df.rename(columns={'index':'Date'})


# In[5]:


df["Date"] = df["Date"].astype(str)
df["Year"] = df["Date"].str.replace("*", "")
df["Month"] = 1
df["Day"] = 1
df["DateOk"] = pd.to_datetime(df[["Year", "Month", "Day"]])

df = df.drop(['Year','Month','Day','Date'], axis=1)
df = df.rename(columns={'DateOk':'Date'})
df = df.set_index('Date')
df.rename_axis(None, axis=1, inplace=True)


# In[7]:


for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# In[8]:


df['country'] = 'CABA'

alphacast.datasets.dataset(664).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




