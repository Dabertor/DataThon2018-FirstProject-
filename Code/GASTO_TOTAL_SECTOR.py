# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 17:53:26 2018

@author: David
"""
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plot

#Lee los datos y 
location=r'C:\Users\David\Desktop\DataThon\Dataset_Wefferent_Card_Analytics\Dataset.txt'
df=pd.read_csv(location,sep="|",parse_dates=['DIA'])

#Reemplazamos las comas por puntos en los importes
df['IMPORTE']=df['IMPORTE'].str.replace(',','.')

#Seleccionamos las columnas que nos intresa
df=df[['DIA','SECTOR','IMPORTE']]


#Generamos un DataFrame que nos de el importe total por sector cada mes
df['DIA']=df['DIA'].map(lambda x: x.strftime('%Y-%m'))
fechas=sorted(list(set(list(df['DIA']))))
sectores=list(set(list(df['SECTOR'])))

df['IMPORTE']=pd.to_numeric(df['IMPORTE'])
df=df.groupby(('DIA','SECTOR'))['IMPORTE'].sum()
#df=df.to_frame().reset_index()


df1=pd.DataFrame(index=fechas,columns=sectores)

for mes in fechas:
    for key,value in df[mes].to_dict().items():
        df1.loc[mes,key]=value

for row in df1.iterrows():
    for sector in range(1,11):
        if math.isnan(row[1][sector])==True:
            row[1][sector]=0

ind=np.arange(len(fechas))
df1.plot(title='Consumo mensual por sector',figsize=(15,10))
plot.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plot.xticks(ind,fechas,rotation=45)
plot.yticks(np.arange(0,2000000,250000),["0","0.25 M","0.5 M","0.75 M","1.00 M","1.25 M","1.50 M","1.75 M"])