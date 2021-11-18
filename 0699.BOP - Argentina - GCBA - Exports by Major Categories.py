#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import io

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[2]:


url = 'https://www.estadisticaciudad.gob.ar/eyc/?p=70399'
page = requests.get(url).text


# In[3]:


soup = BeautifulSoup(page, 'html.parser')


# In[4]:


links = soup.find_all('a')
for link in links:
    if 'xlsx' in link.get('href'):
        link_xls = link.get('href')


# In[5]:


xls_file = requests.get(link_xls).content


# In[6]:


#Guardo en una lista todos los nombres de las hojas
sheet_list = pd.ExcelFile(io.BytesIO(xls_file), engine='openpyxl').sheet_names
#Excluyo las hojas que no corresponden a los años
sheet_list = [sheet for sheet in sheet_list if sheet !='CX_AX05' and sheet !='Ficha técnica']
#Reordeno la lista
sheet_list.reverse()


# In[7]:


#Itero por los nombres de las hojas
for indice, sheet in enumerate(sheet_list):
    df_temp = pd.read_excel(io.BytesIO(xls_file), sheet_name=sheet, engine='openpyxl', skiprows=2)
    df_temp.rename(columns={df_temp.columns[0]:'Rubro', df_temp.columns[1]: 'Total'}, inplace=True)
    
    #En la primera columna elimino la Nota y Fuente
    df_temp['Rubro'] = df_temp['Rubro'].replace('^Nota: ', pd.NA, regex=True)
    df_temp['Rubro'] = df_temp['Rubro'].replace('^Fuente: ', pd.NA, regex=True)
    df_temp.dropna(subset=['Rubro'], inplace=True)
    df_temp['Rubro'] = df_temp['Rubro'].str.strip()
    df_temp.reset_index(drop=True, inplace=True)
    
    #En el caso de 2006 hay una subcategoria duplicada por lo que se la renombra
    if sheet == '2006' and df_temp['Rubro'].str.count("Bebidas,líquidos alcohólico y vinagre").sum() == 2:
        repetido = df_temp[df_temp['Rubro']=="Bebidas,líquidos alcohólico y vinagre"].index[0]
        df_temp.iloc[repetido, 0] = 'Preparados de legumbres y hortalizas'
    
    #Se definen cuales son las categorias principales
    major_items = ['Total', 'Productos Primarios', 'Manufacturas de Origen agropecuario', 
               'Manufacturas de Origen industrial', 'Combustibles y energía']
    
    #Se crea una columna con esos conceptos y se completa el resto de las filas
    df_temp.insert(0, 'Grandes Rubros', pd.NA)

    for item in major_items:
        df_temp['Grandes Rubros'] = np.where(df_temp['Rubro'] == item, item, df_temp['Grandes Rubros'])

    #Completo los NaN en base a la fila previa
    df_temp['Grandes Rubros'].fillna(method='ffill', inplace=True)
    
    #Si coincide el gran rubro con el rubro, mantengo la columna, sino concateno 
    df_temp['Grandes Rubros'] = np.where(df_temp['Rubro'] == df_temp['Grandes Rubros'], 
                            df_temp['Grandes Rubros'], df_temp['Grandes Rubros'] + ' - ' + df_temp['Rubro'])
    
    #Se elimina la primera columna y se establece como indice la columna con las categorias anidadas
    df_temp.drop('Rubro', axis=1, inplace=True)

    df_temp['Date'] = sheet
    df_temp['Date'] = pd.to_datetime(df_temp['Date'], format='%Y', errors='coerce')

    df_temp.set_index('Date', inplace=True)
    
    
    if indice==0:
        df = df_temp.copy()
    else:
        df = df.append(df_temp)


# In[8]:


#Hacemos un primer reemplazo para los grandes rubros
dict_multiples0 = {'Productos Primarios': 'Productos Primarios (PP)',
                 'Manufacturas de Origen agropecuario': 'Manufacturas de Origen agropecuario (MOA)',
                 'Manufacturas de Origen industrial' : 'Manufacturas de Origen industrial (MOI)',
                  'Combustibles y energía': 'Combustibles y energía (CyE)'}


df['Grandes Rubros'] = df['Grandes Rubros'].replace(dict_multiples0, regex=True)


# In[9]:


#Segunda ronda de reemplazos para acortar nombres y homogeneizar rubros que cambian a lo largo de diferentes años
dict_multiples1 = {'^Productos Primarios \(PP\) \-': 'PP -',
                 '^Manufacturas de Origen agropecuario \(MOA\) \-': 'MOA -',
                 '^Manufacturas de Origen industrial \(MOI\) \-': 'MOI -',
                 '^Combustibles y energía \(CyE\) \-' : 'CyE -',
                  'Azúcar ,cacao y artículos de confitería': 'Azúcar, cacao y artículos de confitería',
                  'Azúcar y artículos de confitería': 'Azúcar, cacao y artículos de confitería',
                  'Bebidas,líquidos alcohólico y vinagre':'Bebidas, líquidos alcohólicos y vinagre',
                  'Extractos, curtientes y tintóreos': \
                    'Extractos, curtientes y tintóreos y materias albuminoideas; productos a base de almidón o féculas modificadas, colas enzimas',
                  'Extractos curtientes y tintóreos y materias albuminoideas\;productos a base de almidón o féculas modificadas,colas enzimas': \
                  'Extractos, curtientes y tintóreos y materias albuminoideas; productos a base de almidón o féculas modificadas, colas enzimas',
                  'Grasas y aceites':'Grasas y Aceites',
                  'Preparados de legumbres y hortalizas':'Preparados de legumbres, hortalizas y frutas',
                  'Productos de molinería$':\
                   'Productos de molinería y preparaciones a base de cereales, harina, fécula o leche, productos de pastelería',
                  'Productos de molinería y preparaciones a base de cereales,harina,fécula o leche,productos de pastelería':\
                  'Productos de molinería y preparaciones a base de cereales, harina, fécula o leche, productos de pastelería',
                  'Residuos y desperdicio de ind\.aliment':'Residuos y desperdicios de la industria alimenticia',
                  'Calzado y sus componentes': 'Calzado y sus partes componentes',
                  'Cauchos y sus manufacturas':'Caucho y sus manufacturas',
                  'Manufacturas de cuero, marroquinería$': 'Manufacturas de cuero, marroquinería, etc.',
                  'Manufacturas de piedras, yeso, productos cerámicos, vidrio':\
                  'Manufacturas de piedra, yeso, etc, productos cerámicos, vidrio y sus manufacturas.',
                  'Material de transporte$':'Material de transporte terrestre',
                  'Papel,cartón, imprenta y publicaciones':'Papel, cartón, imprenta y publicaciones',
                  'Papel,cartón,imprenta y publicaciones':'Papel, cartón, imprenta y publicaciones',
                  'Piedras, metales preciosos, monedas':'Piedras, metales preciosos y sus manufacturas, monedas',
                  'Vehiculos de mavegación aérea y marítima':'Vehículos de navegación aérea, marítima y fluvial',
                  'Animales vivos':'Animales Vivos'}

df['Grandes Rubros'] = df['Grandes Rubros'].replace(dict_multiples1, regex=True)

df.iloc[:, 1:].replace('-', 0, inplace=True)


# In[10]:


df['country'] = 'CABA'

alphacast.datasets.dataset(7553).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

