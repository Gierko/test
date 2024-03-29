import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

URL_CSV = 'https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv'
df = pd.read_csv(URL_CSV)
df["continent"] = df.continent.apply(lambda x: x[0:-1])

ALL_CONTINENT = 'All continents'
regions = [ALL_CONTINENT]
regions.extend( list(df.continent.unique()) )

col_title, col_cont, _ = st.columns((5, 5, 4))
with col_title:
  st.title('Car analysis from')
with col_cont:
  selected_region = st.selectbox("", regions )

col1, col2 = st.columns([5,3])

with st.container():

  with col2:
    st.header('Heatmap of car attributes')

    viz = sns.heatmap(
      df.corr(),
      cmap= 'inferno',
      center= 0
    )
    st.write(viz.figure)
    
    st.write('We can see strong correlations all over the place 🍾🥂')

  with col1:
    st.header(f'Weight per horse power')

    ax = plt.subplot()
    viz_bar = sns.scatterplot(
      data= df,
      ax= ax,
      y= 'weightlbs',
      x= 'hp',
      hue= 'time-to-60',
      size= 'cubicinches',
      palette= 'inferno')
    plt.legend( bbox_to_anchor= (1, 1) )

    viz_bar.set_xlabel('Horse power')
   

    st.write( viz_bar.figure )

df_cont = df[['weightlbs', 'hp', 'time-to-60', 'cubicinches', 'continent']]\
  .groupby('continent')\
  .agg('mean')

df_cont.rename( columns= { 'hp': 'Horse Power' }, inplace= True )


with st.container():
  st.title( 'Comparisons by continent' )
  col3, col4, col5 = st.columns(3)
  
  with col3:
    st.header('Horse Power')
    st.bar_chart( df_cont[['Horse Power']] )

  with col4:
    st.header('Cylinders')
    st.bar_chart( df[['cylinders', 'continent']].groupby('continent').agg('median') )

  with col5:
    st.header('Time to 60 (seconds)')
    st.bar_chart( df_cont[['time-to-60']] )
    
 