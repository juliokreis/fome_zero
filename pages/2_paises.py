import utils as utils
import folium
import numpy as np
import pandas as pd
import streamlit as st
import PIL.Image as imgpil
from folium import plugins
import plotly.express as px
from streamlit_folium import folium_static

# ----------------------------------------------------------------

st.set_page_config(page_title='Países', page_icon='🌐', layout='wide')

# ----------------------------------------------------------------
# Chama funções em util.py

# 2. df_raw recebe função 'def extract_data' em utils
df_raw = utils.extract_data()

# 3. Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()

# 4.Função que renomea a colunas
df = utils.rename_columns(df)

# 5.Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(utils.country_name)

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
    country_options = st.sidebar.multiselect('', sorted(set(df['country_code'].unique())),
            default=['Brazil', 'India','United States of America','South Africa'] )
      
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
        # Chama a função 'def cidades_por_pais' para plotar o gráfico de barras
        fig = restaurantes_por_pais(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('Gráfico 3')
        
        