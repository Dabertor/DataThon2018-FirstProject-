# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 17:03:55 2018

@author: David
"""
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plot

location= r'C:\Users\David\Desktop\DataThon\Dataset_Wefferent_Card_Analytics\Dataset.txt'
df=pd.read_csv(location,sep="|",parse_dates=['DIA'])


CP=[]
sectores=set(df['SECTOR'])
diccionario={}

#Reemplazamos las ',' por los '.' para poder operar
df['IMPORTE']=df['IMPORTE'].str.replace(',','.')

#Parseamos a numerico el importe
df['IMPORTE']=pd.to_numeric(df['IMPORTE'])

#Queremos sacar los CP_CLIENTE que mas se han gastado
cpRicos=df.groupby(('CP_CLIENTE'))[['IMPORTE']].sum()
cpRicos=cpRicos.sort_values(['IMPORTE'],ascending=[0]).head(10)
CP=cpRicos.index.values

#Filtramos los CP_CLIENTES que mas gastan
#df_filtered=df[(df.CP_CLIENTE==30000)]
df_filtered=df.loc[df['CP_CLIENTE'].isin(CP)]

#Agrupamos por CP_CLiente y Sector y el conjunto de importes, lo sumamos
df_filtered=df_filtered.groupby(('CP_CLIENTE','SECTOR'))['IMPORTE'].sum()

df1=pd.DataFrame(index=CP,columns=sectores)

for cp in CP:
    for key,value in df_filtered[cp].to_dict().items():
        df1.loc[cp,key]=value

for row in df1.iterrows():
    for sector in range(1,11):
        if math.isnan(row[1][sector])==True:
            row[1][sector]=0     
            
df1.plot(kind='bar',stacked='True',title='consumo/sectore en CP_CLIENTE que más gastan',figsize=(10,10))
plot.yticks(np.arange(0,15000000,2000000),["0","2 M","4 M","6 M","8 M","10 M","12 M","14 M"])
plot.colorbar()