# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:32:30 2018

@author: David
"""
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns

#Lee los datos y 
location=r'C:\Users\David\Desktop\DataThon\Dataset_Wefferent_Card_Analytics\Dataset.txt'
df=pd.read_csv(location,sep="|",parse_dates=['DIA','SECTOR'])

CP=[30009]
df_filtered=df[['CP_COMERCIO','SECTOR','NUM_OP','PROP_R_BAJA','PROP_R_MEDIA','PROP_R_ALTA']]
df_filtered=df_filtered.loc[df['CP_COMERCIO'].isin(CP)]

str_cols=['PROP_R_BAJA','PROP_R_MEDIA','PROP_R_ALTA']
df_filtered[str_cols]=df_filtered[str_cols].replace(',', '.', regex=True)
df_filtered['PROP_R_BAJA']=pd.to_numeric(df_filtered['PROP_R_BAJA'])
df_filtered['PROP_R_MEDIA']=pd.to_numeric(df_filtered['PROP_R_MEDIA'])
df_filtered['PROP_R_ALTA']=pd.to_numeric(df_filtered['PROP_R_ALTA'])

sectores=list(set(list(df['SECTOR'])))


def multRentB(row):
    return int(round(row['PROP_R_BAJA']*row['NUM_OP']))

def multRentM(row):
    return int(round(row['PROP_R_MEDIA']*row['NUM_OP']))

def multRentA(row):
    return int(round(row['PROP_R_ALTA']*row['NUM_OP']))

df_filtered['PROP_R_BAJA']=df_filtered.apply(multRentB,axis=1)
df_filtered['PROP_R_MEDIA']=df_filtered.apply(multRentM,axis=1)
df_filtered['PROP_R_ALTA']=df_filtered.apply(multRentA,axis=1)
df_filtered=df_filtered[['SECTOR','PROP_R_BAJA','PROP_R_MEDIA','PROP_R_ALTA']]

df1=pd.DataFrame(index=sectores,columns=str_cols,data=0)

contador=0
for linea in df_filtered.iterrows():
    
    if linea[1][1]!=0:
        df1.loc[[linea[1][0]],['PROP_R_BAJA']]+=linea[1][1]    
    
    if linea[1][2]!=0:
        df1.loc[[linea[1][0]],['PROP_R_MEDIA']]+=linea[1][2] 
        
    if linea[1][3]!=0:
        df1.loc[[linea[1][0]],['PROP_R_ALTA']]+=linea[1][3]
    
    contador+=1
    print(contador)

#df1.plot(title='NºOp según la renta en CP_COMERCIO 30009',figsize=(10,10))
df1.plot.pie(subplots=True,figsize=(40,10),autopct='%.2f')