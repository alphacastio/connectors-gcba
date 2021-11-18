#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

# In[ ]:


# get html from site and write to local file
url = "https://www.estadisticaciudad.gob.ar/eyc/?p=28446"
r = requests.get(url,verify=False)
html = r.content
htmlparser = etree.HTMLParser()
tree = etree.fromstring(html, htmlparser)
xls_address = tree.xpath("//*[@id='post-28446']/div/a/@href")[0]


# In[ ]:


r = requests.get(xls_address, allow_redirects=True, verify=False)
df = pd.read_excel(r.content, skiprows=2, sheet_name=0)


# In[ ]:


df = df.dropna(how='all', subset = df.columns[1:])
df = df.set_index('Unnamed: 0')
df = df.T.reset_index()
df.rename_axis(None, axis=1, inplace=True)
df = df.rename(columns={'index':'Date'})


# In[ ]:


df['Date'] = df['Date'].replace('\*', '', regex=True)

dict_months = {"ene": "01-01", "feb": "02-01","mar": "03-01","abr": "04-01", "may": "05-01",
               "jun": "06-01","jul": "07-01","ago": "08-01", "sep": "09-01", "oct": "10-01", 
               "nov": "11-01","dic": "12-01"}
df['Date'] = df['Date'].replace(dict_months, regex=True)
df['Date'] = pd.to_datetime(df['Date'])

df = df.set_index('Date')
df['country'] = 'CABA'

alphacast.datasets.dataset(662).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)




