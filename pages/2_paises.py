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

# 2. df_raw recebe função 'def extract_data' em utils
df_raw = us.extract_data()

# 3. Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()

# 4.Função que renomea a colunas
df = us.rename_columns(df)

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
# FUNÇÕES 

# DE TROCA
# 4.Função que gera o código ao nome de cada pais
df['country_name'] = df['country_code'].apply(us.country_name)

# GRÁFICAS

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
    fig = px.bar(pais, x='country_code',y='restaurant_id',
                title='Quantidade de cidades por País',
                labels={'country_code': 'País', 'restaurant_id': 'Qtde de restaurantes'})
    fig.update_traces(texttemplate = '%{y}')
    return fig

def nivel_4(df):
    df['price_type'] = df.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))

    price_type_counts = df['price_type'].value_counts().reset_index()
    price_type_counts.columns = ['price_type', 'count']
    df.sort_values(by='count', ascending=False)
    
    # grafico de barras
    fig = px.bar(df, x='country_name',y='restaurant_id',
                title='Países com restaurantes nível 4',
                labels={'country_name': 'País', 'restaurant_id': 'Qtde de restaurantes'})
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

    country_options = st.sidebar.multiselect('', sorted(set(df['country_name'].unique())),
    default=['Brazil', 'India','United States of America','South Africa', 'Canada'] )
    
    linhas_selecionadas = df['country_name'].isin(country_options)
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
        # Chama a função 'def cidades_por_pais' para plotar o gráfico de barras
        fig = restaurantes_por_pais(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('Gráfico 3')
        # Chama a função 'def cidades_por_pais' para plotar o gráfico de barras
        fig = nivel_4(df)
        st.plotly_chart(fig, use_container_width=True)

        
        
