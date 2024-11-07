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

# df_raw recebe função 'def extract_data' em utils
df_raw = us.extract_data()

# Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()

# Função que renomea a colunas
df = us.rename_columns(df)

# Função que renomea a colunas
df = us.rename_columns(df)

# Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(us.country_name)

# Função que categoriza a comida peloa faixa de preço
df['price_type'] = df.loc[:, 'price_range'].apply(lambda x: us.create_price_tye(x))


# # caminho relativo (deploy)
# def extract_data(path='data/zomato.csv'):
#     return pd.read_csv(path)

# # 1.Função que lê o dataframe
# df = extract_data()

# # 2. Chama a função que extraiu o dataframe
# df = extract_data
# df_raw = extract_data()

# # 3. Copia o dataframe original (df_raw) para o de trabalho (df)
# df = df_raw.copy()


# ------------------------------------------------------------------------------------------
# FUNÇÕES GRÁFICAS

# 1. Qual o nome do país que possui mais cidades registradas?
def city_country(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    pais = df.groupby('country_code')['city'].nunique().sort_values(ascending=False).reset_index()

    # gráfico
    fig = px.bar(pais, x=pais['country_code'], y=pais['city']
                 ,title='Quantidade de cidades por País'
                 ,labels={'country_code': 'País', 'city': 'Qtde Cidades'})
    fig.update_traces(texttemplate = '%{y}') 
    return fig
    
# 2. Qual o nome do país que possui mais restaurantes registrados?
def restaurant_country(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    country=(df.groupby('country_code')['restaurant_id']
            .nunique()
            .sort_values(ascending=False)
            .reset_index())

    # gráfico
    fig = px.bar(country, x=country['country_code'], y=country['restaurant_id']
                 ,title='Quantidade de cidades por País'
                 ,labels={'country_code': 'País', 'restaurant_id': 'Qtde de restaurantes'})
    fig.update_traces(texttemplate = '%{y}')
    return fig


# 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
def level_price(df): 
    level_price=(df.loc[df['price_range'] == 4, ['restaurant_id', 'country_code']]
                 .groupby('country_code')
                 .count()
                 .sort_values('restaurant_id', ascending=False)
                 .reset_index())
    # gráfico
    fig = px.bar(level_price, x=level_price['country_code'],y=level_price['restaurant_id']
                 ,title='Países com restaurantes nível 4'
                 ,labels={'country_code': 'País', 'restaurant_id': 'Qtde restaurant gourmet'})
    fig.update_traces(texttemplate = '%{y}')
    return fig

# ------------------------------------------------------------------------------------------
# SIDEBAR

image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
st.sidebar.markdown('### Escolha o país.')
st.sidebar.markdown('''---''')

with st.sidebar.container():
    st.markdown('## VISÃO PAÍSES')

    country_options = st.sidebar.multiselect('', sorted(set(df['country_code'].unique())),
    default=['Brazil', 'India','United States of America','South Africa', 'Canada'] )
    
    linhas_selecionadas = df['country_name'].isin(country_options)
    df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')

# ------------------------------------------
# LAYOUT STREAMLIT

with st.container():
    # Chama a função 'def city_country' para plotar o gráfico de barras
    fig = city_country(df)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Chama a função 'def restaurant_country' para plotar o gráfico de barras
        fig = restaurant_country(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Chama a função 'def level_price' para plotar o gráfico de barras
        fig = level_price(df)
        st.plotly_chart(fig, use_container_width=True)

        
        
