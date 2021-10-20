import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import plotly

df=pd.read_csv('first.csv')

def frequency():
    numbers=df['PHONE'].astype('str').value_counts().head(10).index
    freq=df['PHONE'].value_counts().head(10)
    plt.bar(numbers,freq)
    plt.xticks(numbers,numbers,rotation=70)
    plt.ylabel('Number of times Called',weight='bold')
    plt.xlabel('Phone Numbers',weight='bold')
frequency()

def typeofcall():
    plt.bar(df['TYPE'].value_counts().index,df['TYPE'].value_counts())
typeofcall()

def addcol():
    duration=[]
    daynight=[]
    for i in range(100):
        start=datetime.datetime.strptime(df['START'][i],'%Y-%m-%d %H:%M:%S')
        end=datetime.datetime.strptime(df['END'][i],'%Y-%m-%d %H:%M:%S')
        duration.append(end-start)
        if(start.hour<20 and start.hour>4):
            daynight.append('DAY')
        else: 
            daynight.append('NIGHT')
    df['DURATION']=duration        
    df['DAY/NIGHT']=daynight
    
def daynight():
  addcol()
  px.scatter_geo(df['PHONE'],lat=df['LATITUDE'],lon=df['LONGITUDE'],color=df['DAY/NIGHT'])

def typecallmap():
  px.scatter_geo(df['PHONE'],lat=df['LATITUDE'],lon=df['LONGITUDE'],color=df['TYPE'])

def imei():
  imei=[]
  for i in df['IMEI1']:
      imei.append(str(i))
  px.scatter_geo(df['PHONE'],lat=df['LATITUDE'],lon=df['LONGITUDE'],color=imei)

