# **Unemployment analysis using Python**

"""# Importing Libraries"""


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import plotly.express as px

"""# Data Import"""

unemp = pd.read_csv('/content/Unemployment_Rate_upto_11_2020.csv')
unemp.head(2)

unemp.info()

unemp.isnull().sum()

#renaming column names for better understanding
unemp.columns =['States','Date','Frequency','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate','Region','longitude','latitude']
unemp.head(2)

#converting date column datatype to datetime format since it is in object type
unemp['Date'] = pd.to_datetime(unemp['Date'],dayfirst=True)

unemp['Frequency']= unemp['Frequency'].astype('category')

unemp['Month'] =  unemp['Date'].dt.month

unemp['Month_int'] = unemp['Month'].apply(lambda x : int(x))

unemp['Month_name'] =  unemp['Month_int'].apply(lambda x: calendar.month_abbr[x])

unemp['Region']= unemp['Region'].astype('category')

unemp.info()

unemp.drop(columns='Month',inplace=True)    #dropped Month column

"""# Stats"""

unemp_stats = unemp[['Estimated Unemployment Rate',
       'Estimated Employed', 'Estimated Labour Participation Rate']]


round(unemp_stats.describe(),2)

region_stats = unemp.groupby(['Region'])[['Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']].mean().reset_index()

region_stats = round(region_stats,2)


region_stats

"""# Data Visualization"""

fig = px.box(unemp,x='States',y='Estimated Unemployment Rate',color='States',title='Unemployment rate',template='plotly')
fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.show()

plot_ump = unemp[['Estimated Unemployment Rate','States']]

df_unemp = plot_ump.groupby('States').mean().reset_index()

df_unemp = df_unemp.sort_values('Estimated Unemployment Rate')

fig = px.bar(df_unemp, x='States',y='Estimated Unemployment Rate',color='States',
            title='Average Unemployment Rate in each state',template='plotly')

fig.show()

fig = px.bar(unemp, x='Region',y='Estimated Unemployment Rate',animation_frame = 'Month_name',color='States',
            title='Unemployment rate across region from Jan.2020 to Oct.2020', height=700,template='plotly')

fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.show()

unemplo_df = unemp[['States','Region','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']]

unemplo = unemplo_df.groupby(['Region','States'])['Estimated Unemployment Rate'].mean().reset_index()


fig = px.sunburst(unemplo, path=['Region','States'], values='Estimated Unemployment Rate',
                  color_continuous_scale='Plasma',title= 'unemployment rate in each region and state',
                  height=500,template='plotly')


fig.show()

lock = unemp[(unemp['Month_int'] >= 4) & (unemp['Month_int'] <=7)]

bf_lock = unemp[(unemp['Month_int'] >= 1) & (unemp['Month_int'] <=4)]

g_lock = lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()

g_bf_lock = bf_lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()


g_lock['Unemployment Rate before lockdown'] = g_bf_lock['Estimated Unemployment Rate']

g_lock.columns = ['States','Unemployment Rate after lockdown','Unemployment Rate before lockdown']

g_lock.head(2)

g_lock['percentage change in unemployment'] = round(g_lock['Unemployment Rate after lockdown'] - g_lock['Unemployment Rate before lockdown']/g_lock['Unemployment Rate before lockdown'],2)

plot_per = g_lock.sort_values('percentage change in unemployment')

fig = px.bar(plot_per, x='States',y='percentage change in unemployment',color='percentage change in unemployment',
            title='percentage change in Unemployment in each state after lockdown',template='ggplot2')

fig.show()

def sort_impact(x):
    if x <= 10:
        return 'impacted States'
    elif x <= 20:
        return 'hard impacted States'
    elif x <= 30:
        return 'harder impacted States'
    elif x <= 40:
        return 'hardest impacted States'
    return x

plot_per['impact status'] = plot_per['percentage change in unemployment'].apply(lambda x:sort_impact(x))

fig = px.bar(plot_per, y='States',x='percentage change in unemployment',color='impact status',
            title='Impact of lockdown on employment across states',template='ggplot2',height=650)


fig.show()
