import utils as us
import pandas as pd
import numpy as np
import PIL.Image as imgpil
import streamlit as st
import folium

from folium.plugins import MarkerCluster
from folium import plugins
from streamlit_folium import folium_static
# ----------------------------------------------------------------

st.set_page_config(
    page_title='Visão geral',
    page_icon='👁️',
    layout='wide',
    initial_sidebar_state='auto'
)

# ----------------------------------------------------------------
# Leitura do dataframe bruto

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

# ----------------------------------------------------------------
# Chamada das funções no util.py

# 3.Função que renomea a colunas
df = us.rename_columns(df)

# 4.Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(us.country_name)

# ------------------------------------------------------------------------------------------
# FUNÇÃO PARA PLOTAR MAPA

def geolocal(df):
    mapa = (df.loc[:, ['country_code', 'city', 'latitude', 'longitude', 'restaurant_name', 'cuisines']]
            .groupby(['country_code', 'city', 'restaurant_name'])
            .value_counts().reset_index().sample(1000))

    mapa_coordenadas = folium.Map(location=[5.9658, -11.6016],use_container_width=True , zoom_start=2)

    agrupador = MarkerCluster().add_to(mapa_coordenadas)

    for index, location_info in mapa.iterrows():
        (folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                       popup=location_info[['country_code','city', 'restaurant_name', 'cuisines']])
                       .add_to(agrupador))

    mapa_coordenadas.add_child(folium.LatLngPopup()) 
    folium_static(mapa_coordenadas, width=1024, height=600)


# ------------------------------------------------------------------------------------------
# SIDEBAR

image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
st.markdown('### Escolha o país.')
country_options = st.sidebar.multiselect('', sorted(set(df['country_code'].unique())),
    default=['Brazil', 'India','United States of America','South Africa', 'Canada'] )
    
linhas_selecionadas = df['country_code'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')


# ------------------------------------------
# LAYOUT STREAMLIT

st.header('Visão Geral')
with st.container():   
    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='center')
    with col1:
        restaurantes = df['restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados', restaurantes)
        # 1. Quantos restaurantes únicos estão registrados?
        # st.markdown('Restaurantes cadastrados')

    with col2:
        # 2. Quantos países únicos estão registrados?
        # st.markdown('Países')
        paises = df['country_code'].nunique()
        col2.metric('Países cadastrados', paises)
    with col3:
        # 3. Quantas cidades únicas estão registradas?
        # st.markdown('Cidades')
        cidades = df['city'].nunique()
        col3.metric('Cidades cadastradas', cidades)
    with col4:
        # 4. Qual o total de avaliações feitas?
        # (As avaliações são feitas pela quantidade de votos)
        # st.markdown('Avaliações')
        avaliacoes = df['votes'].sum()
        col4.metric('Avaliações', avaliacoes)
    with col5:
        # 5. Qual o total de tipos de culinária registrados?
        # st.markdown('Culinárias')
        culinaria = df['cuisines'].nunique()
        col5.metric('Culinária', culinaria)

    st.markdown(''' ---''')

with st.container():
    st.markdown('## Distribuição dos restaurantes pelo mundo')
    # Geolocalização
    # Chama a função 'def geolocal' para plotar o mapa
    # st.markdown('localização central de cidade')
    geolocal(df)

