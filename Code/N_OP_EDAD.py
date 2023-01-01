# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:32:30 2018

@author: David
"""
import pandas as pd
import matplotlib.pyplot as plot

#Lee los datos y 
location=r'C:\Users\David\Desktop\DataThon\Dataset_Wefferent_Card_Analytics\Dataset.txt'
df=pd.read_csv(location,sep="|",parse_dates=['DIA','SECTOR'])

CP=[30009]
df_filtered=df[['CP_COMERCIO','SECTOR','NUM_OP','PROP_JOVEN','PROP_ADULTO','PROP_PENSIONISTA']]
df_filtered=df_filtered.loc[df['CP_COMERCIO'].isin(CP)]
df_filtered['PROP_JOVEN']=df_filtered['PROP_JOVEN'].str.replace(',','.')
df_filtered['PROP_ADULTO']=df_filtered['PROP_ADULTO'].str.replace(',','.')
df_filtered['PROP_PENSIONISTA']=df_filtered['PROP_PENSIONISTA'].str.replace(',','.')
df_filtered['PROP_JOVEN']=pd.to_numeric(df_filtered['PROP_JOVEN'])
df_filtered['PROP_ADULTO']=pd.to_numeric(df_filtered['PROP_ADULTO'])
df_filtered['PROP_PENSIONISTA']=pd.to_numeric(df_filtered['PROP_PENSIONISTA'])

sectores=list(set(list(df['SECTOR'])))
tipoEdad=['joven','adulto','pensionista']

def multRentB(row):
    return int(round(row['PROP_JOVEN']*row['NUM_OP']))

def multRentM(row):
    return int(round(row['PROP_ADULTO']*row['NUM_OP']))

def multRentA(row):
    return int(round(row['PROP_PENSIONISTA']*row['NUM_OP']))

df_filtered['PROP_JOVEN']=df_filtered.apply(multRentB,axis=1)
df_filtered['PROP_ADULTO']=df_filtered.apply(multRentM,axis=1)
df_filtered['PROP_PENSIONISTA']=df_filtered.apply(multRentA,axis=1)
df_filtered=df_filtered[['SECTOR','PROP_JOVEN','PROP_ADULTO','PROP_PENSIONISTA']]

df1=pd.DataFrame(index=sectores,columns=tipoEdad,data=0)
print(df1)
contador=0
for linea in df_filtered.iterrows():

    if linea[1][1]!=0:
        df1.loc[[linea[1][0]],['joven']]+=linea[1][1]    
    
    if linea[1][2]!=0:
        df1.loc[[linea[1][0]],['adulto']]+=linea[1][2] 
        
    if linea[1][3]!=0:
        df1.loc[[linea[1][0]],['pensionista']]+=linea[1][3]
    
    contador+=1
    print(contador)
#df1.loc[tipoRenta[0],['ALIMENTACION']]=df_filtered.loc[[1139],[1]]

print(df1)
#df1.plot(title='NºOp según la edad en CP_COMERCIO 30009',figsize=(10,10))
df1.plot.pie(subplots=True,figsize=(40,10),autopct='%.2f')