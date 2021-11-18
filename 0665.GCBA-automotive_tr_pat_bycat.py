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

# In[23]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/AC_AU_AX06.xlsx"
df1 = pd.read_excel(url1)
df1[:1] = df1[:1].ffill(1)
df1.columns =  "Transferencias de automotores - " + df1.iloc[0]
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=0)
df1 = df1.dropna(subset = ['Transferencias de automotores - Total'])
df1 = df1[~df1.iloc[:, 0].astype(str).str.isdigit()]
df1 = df1.drop(df1.columns[[0]], axis=1)
df1.index = pd.date_range(start='1/1/2016', periods=len(df1), freq = "QS")
df1.index.name = "Date"
#df1 = df1[df1.columns.drop(list(df1.filter(regex='Participación')))]


# In[34]:


url2 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/AC_AU_AX05.xlsx"
df2 = pd.read_excel(url2)
#df2[:1] = df2[:1].ffill(1)
df2.columns =  "Distribución de patentamientos de automotores - " + df2.iloc[0]
df2 = df2.drop(index=0)
df2 = df2.drop(index=1)
#df2 = df2.drop(index=2)
df2 = df2.dropna(subset = ['Distribución de patentamientos de automotores - Persona jurídica'])
df2 = df2[~df2.iloc[:, 0].astype(str).str.isdigit()]
df2 = df2.drop(df2.columns[[0]], axis=1)
df2 = df2.drop(df2.columns[[0]], axis=1)
df2.index = pd.date_range(start='1/1/2016', periods=len(df2), freq = "QS")
df2.index.name = "Date"


# In[41]:


url3 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/AC_AU_AX04.xlsx"
df3 = pd.read_excel(url3)
#df3[:1] = df3[:1].ffill(1)
df3.columns =  "Distribución de patentamientos de automotores - " + df3.iloc[0]
df3 = df3.drop(index=0)
df3 = df3.drop(index=1)
#df3 = df3.drop(index=2)
df3 = df3.dropna(subset = [df3.columns[3]])
df3 = df3[~df3.iloc[:, 0].astype(str).str.isdigit()]
df3 = df3.drop(df3.columns[[0]], axis=1)
df3 = df3.drop(df3.columns[[0]], axis=1)
df3.index = pd.date_range(start='1/1/2016', periods=len(df3), freq = "QS")
df3.index.name = "Date"


# In[52]:


url4 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/AC_AU_AX03.xlsx"
df4 = pd.read_excel(url4)
df4[:1] = df4[:1].ffill(1)
df4.columns =  "Patentamiento de automotores - " + df4.iloc[0] + " - " + df4.iloc[1]
df4 = df4.drop(index=0)
df4 = df4.drop(index=1)
#df4 = df4.drop(index=2)
df4 = df4.dropna(subset = [df4.columns[7]])
df4 = df4[~df4.iloc[:, 0].astype(str).str.isdigit()]
df4 = df4.loc[:, df4.columns.notnull()]
df4.index = pd.date_range(start='1/1/2016', periods=len(df4), freq = "QS")
df4.index.name = "Date"


# In[54]:


df5 = df1.merge(df2, right_index = True, left_index=True, how = "left").merge(df3, right_index = True, left_index=True, how = "left").merge(df4, right_index = True, left_index=True, how = "left")
df5["country"] = "CABA"

alphacast.datasets.dataset(663).upload_data_from_df(df5, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[ ]:




