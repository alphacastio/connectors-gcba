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

# In[6]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_horas_trabajadas.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"

alphacast.datasets.dataset(7437).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)



# In[7]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_masa_salarial.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"

alphacast.datasets.dataset(7438).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[8]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_salario_medio.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"


alphacast.datasets.dataset(7439).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[9]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_intensidad_laboral.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"


alphacast.datasets.dataset(7440).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[10]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_personal_asalariado.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"


alphacast.datasets.dataset(7441).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)


# In[11]:


url1 = "https://www.estadisticaciudad.gob.ar/eyc/wp-content/uploads/2018/05/ee_industria_ingresos_fabriles.xlsx"
df1 = pd.read_excel(url1)
df1[:2] = df1[:2].ffill(1)
df1.columns =   df1.iloc[0] + " - " + df1.iloc[1] 
df1 = df1.drop(index=1)
df1 = df1.drop(index=0)
#df1 = df1.drop(index=2)
#df1 = df1.drop(index=3)
df1 = df1.dropna(subset = [df1.columns[3]])
df1 = df1[df1.columns.dropna()]
df1.index = pd.date_range(start='10/1/2001', periods=len(df1), freq = "MS")
df1.index.name = "Date"
df1["country"]="CABA"

alphacast.datasets.dataset(7442).upload_data_from_df(df1, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

