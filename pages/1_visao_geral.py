from utils.functions import *
import pandas as pd
import numpy as np
import PIL.Image as imgpil
import streamlit as st
import folium
import inflection
from streamlit_folium import folium_static

st.set_page_config(page_title='Home', page_icon='🏠', layout='wide')


# 1. Extrai o dataframe, em seguida leitura do arquivo csv
def extract_data(path='data/zomato.csv'):
    return pd.read_csv(path)


# 2. Chama a função que extraiu o dataframe
df = extract_data
df_raw = extract_data()


# 3. Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()
# ----------------------------------------------------------------

df = rename_columns(df)

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
    # st.title('Map')
    # df_aux = (df.loc[:, ['country_code','city','latitude',
    #                     'longitude','restaurant_name']]
    #                     .groupby(['country_code','city','restaurant_name'])
    #                     .value_counts().reset_index()).sample(10)
    # df_aux
    # # df_aux = df_aux.loc[df_aux['city'] != 'Nan',:]
    # # df_aux = df_aux.loc[df_aux['country_code'] != 'Nan',:]

    # map = folium.Map()
    
    # for index, location_info in df_aux.iterrows():
    #     folium.Marker([location_info['latitude'],
    #                     location_info['longitude']],
    #                     popup=location_info[['latitude','longitude']]).add_to(map)
        
    # folium_static(map, width=1024, height=600)

    st.markdown('### Distribuição dos restaurantes pelo mundo')
    mapa = (df.loc[:, ['country_code','city','latitude','longitude','restaurant_name', 'cuisines']]
                        .groupby(['country_code','city','restaurant_name'])
                        .value_counts().reset_index().head(500))
 
    mapa_coordenadas = folium.Map(zoom_start=5, control_scale=True, 
                    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
                    attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012')

    folium.TileLayer('cartodbpositron').add_to(mapa_coordenadas)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
                     attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
                     name= 'Esri.WorldStreetMap').add_to(mapa_coordenadas)
    folium.LayerControl().add_to(mapa_coordenadas)

    # for i in range(len(map)):
    #     coordenadas = mapa[i]
    #     local = mapa[i]
    #     folium.Marker(coordenadas).add_to(mapa)
    # mapa

    for index, location_info in mapa.iterrows():
        (folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                        popup=location_info[['city','restaurant_name', 'cuisines']], 
                        icon=folium.Icon(icon='glyphicon glyphicon-cutlery'))
                        .add_to(mapa_coordenadas))
        
    folium_static(mapa_coordenadas, width=1024, height=600)
    


