import utils as us
import folium
import numpy as np
import pandas as pd
import streamlit as st
import PIL.Image as imgpil
from folium import plugins
import plotly.express as px
from streamlit_folium import folium_static

# ----------------------------------------------------------------

# st.set_page_config(page_title='Países', page_icon='🌐', layout='wide')

# ----------------------------------------------------------------
# Chama funções em util.py

# caminho relativo (deploy)
def extract_data(path='data/zomato.csv'):
    return pd.read_csv(path)

# 1.Função que lê o dataframe
df = extract_data()

# 2. Chama a função que extraiu o dataframe
df = extract_data
df_raw = extract_data()

# 3. Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()
# ------------------------------------------------------------------------------------------
# FUNÇÕES GRÁFICAS

def cidades_por_pais(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    pais = df.groupby('country_code')['city'].nunique().sort_values(ascending=False).reset_index()

    # gráfico
    fig = px.bar(pais, x=pais['country_code'], y=pais['city'])
    fig = px.bar(pais, x='country_code',y='city',
                title='Quantidade de cidades por País',
                labels={'country_code': 'País', 'city': 'Qtde Cidades'})
    fig.update_traces(texttemplate = '%{y}') 
    return fig


def restaurantes_por_pais(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    pais = df.groupby('country_code')['restaurant_id'].nunique().sort_values(ascending=False).reset_index()

    # gráfico
    fig = px.bar(pais, x='country_code', y='restaurant_id')
    fig = px.bar(pais, x='country_code',y='restaurant_id',
                title='Quantidade de cidades por País',
                labels={'country_code': 'País', 'restaurant_id': 'Qtde de restaurantes'})
    fig.update_traces(texttemplate = '%{y}')
    return fig

# ------------------------------------------------------------------------------------------
# SIDEBAR

image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
st.sidebar.markdown('### Escolha o país.')
st.sidebar.markdown('''---''')

with st.container():
    st.markdown('## VISÃO PAÍSES')

    # Filtro multiseletor de paises

    df['country_name'] = df['country_code'].apply(country_name).unique()
    country_options = st.sidebar.multiselect('', sorted(set(df['country_name'].unique())),
    default=['Brazil', 'India','United States of America','South Africa', 'Canada'] )
    
    linhas_selecionadas = df['country_code'].isin(country_options)
    df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')

# ------------------------------------------
# LAYOUT STREAMLIT

with st.container():
    # Chama a função 'def cidades_por_pais' para plotar o gráfico de barras
    fig = cidades_por_pais(df)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Gráfico 2')
        # # Chama a função 'def cidades_por_pais' para plotar o gráfico de barras
        # fig = restaurantes_por_pais(df)
        # st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('Gráfico 3')
        
        
