# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:32:16 2018

@author: David
"""
import pandas as pd
import math
import matplotlib.pyplot as plot
import numpy as np

location= r'C:\Users\David\Desktop\DataThon\Dataset_Wefferent_Card_Analytics\Dataset.txt'
df=pd.read_csv(location,sep="|",parse_dates=['DIA'])


CP=[]
sectores=set(df['SECTOR'])
diccionario={}

#Reemplazamos las ',' por los '.' para poder operar
df['IMPORTE']=df['IMPORTE'].str.replace(',','.')

#Parseamos a numerico el importe
df['IMPORTE']=pd.to_numeric(df['IMPORTE'])

#Queremos sacar los CP_COMERCIO donde mas se ha gastado
masConsumo=df.groupby(('CP_COMERCIO'))[['IMPORTE']].sum()
masConsumo=masConsumo.sort_values(['IMPORTE'],ascending=[0]).head(10)
CP=masConsumo.index.values

#Filtramos los CP_COMERCIO donde más se gasta
df_filtered=df.loc[df['CP_COMERCIO'].isin(CP)]

#Agrupamos por CP_CLiente y Sector y el conjunto de importes, lo sumamos
df_filtered=df_filtered.groupby(('CP_COMERCIO','SECTOR'))['IMPORTE'].sum()

df1=pd.DataFrame(index=CP,columns=sectores)

for cp in CP:
    for key,value in df_filtered[cp].to_dict().items():
        df1.loc[cp,key]=value

for row in df1.iterrows():
    for sector in range(1,11):
        if math.isnan(row[1][sector])==True:
            row[1][sector]=0         

df1.plot(kind='bar',stacked='True',title='consumo/sectore en CP_COMERCIO donde más se gasta',figsize=(10,10))
plot.yticks(np.arange(0,35000000,5000000),["0","5 M","10 M","15 M","20 M","25 M","30 M"])