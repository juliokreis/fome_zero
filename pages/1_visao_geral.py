# from util import *
import inflection

import pandas as pd
import numpy as np
import PIL.Image as imgpil
import streamlit as st
import folium
from streamlit_folium import folium_static
# ----------------------------------------------------------------

st.set_page_config(page_title='Home', page_icon='🏠', layout='wide')


# 1. Extrai o dataframe, em seguida leitura do arquivo csv
def extract_data(path='/home/jcr/projetos/fome_zero/data/zomato.csv'):
    return pd.read_csv(path)


# 2. Chama a função que extraiu o dataframe
df = extract_data
df_raw = extract_data()


# 3. Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()

# ----------------------------------------------------------------
# FUNCTIONS

# 1.Função que categoriza a comida peloa faixa de preço


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
# df = create_price_tye(df)


# 2.Função classifica o restaurante conforme a cor. Quanto mais claro melhor.
def color_name(color_code):
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    return COLORS[color_code]
# df = color_name(df)


# 3.Função que renomea a colunas
def rename_columns(df_raw):
    df = df_raw.copy()
    def title(x): return inflection.titleize(x)
    def snakecase(x): return inflection.underscore(x)
    def spaces(x): return x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


# 4.Função que gera o código ao nome de cada pais
def country_name(country_code):
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America"
    }
    return COUNTRIES[country_code]


# ----------------------------------------------------------------
# Chamada das funções no util.py

# 3.Função que renomea a colunas
df = rename_columns(df)

# 4.Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(country_name)


# ------------------------------------------------------------------------------------------
# SIDEBAR
image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

st.sidebar.markdown('# Escolha o país.')
country_options = st.sidebar.multiselect('',
                                         ['Austrália', 'Brazil', 'Canada', 'England',
                                          'Índia', 'Indonésia', 'New Zeland', 'Philippines',
                                          'Qatar', 'Singapure', 'South Africa', 'Sri Lanka',
                                          'Turkey', 'United Arab Emirates',
                                          'United States of America'],
                                         default=['Austrália', 'Brazil', 'Canada', 'England'])

# ------------------------------------------
# LAYOUT STREAMLIT

st.header('Visão Geral')
with st.container():
    st.markdown('coloque as métricas abaixo')
    col1, col2, col3, col4, col5 = st.columns(spec=[0.5, 0.4, 0.4, 0.5, 0.3])
    with col1:
        # 1. Quantos restaurantes únicos estão registrados?
        # st.markdown('Restaurantes cadastrados')
        restaurantes = df['restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados', restaurantes)

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
    st.markdown('### Distribuição dos restaurantes pelo mundo')
    mapa = (df.loc[:, ['country_code', 'city', 'latitude', 'longitude', 'restaurant_name', 'cuisines']]
            .groupby(['country_code', 'city', 'restaurant_name'])
            .value_counts().reset_index().head(500))

    mapa_coordenadas = folium.Map()
    for index, location_info in mapa.iterrows():
        (folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                       popup=location_info[['city', 'restaurant_name', 'cuisines']])
         .add_to(mapa_coordenadas))

    folium_static(mapa_coordenadas, width=1024, height=600)
