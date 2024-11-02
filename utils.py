import pandas as pd
import numpy as np
import PIL.Image as imgpil
import streamlit as st
import inflection
import folium
import plotly.express as px
from folium import plugins
from streamlit_folium import folium_static


# ----------------------------------------------------------------

st.set_page_config(page_title='Home', page_icon='🏠', layout='wide')

# ----------------------------------------------------------------
# FUNCTIONS

# 1. Extrai o dataframe, em seguida leitura do arquivo csv


# caminho absoluto (teste)
# def extract_data(path='/home/jcr/projetos/fome_zero/data/zomato.csv'):
#     return pd.read_csv(path)

# caminho relativo (deploy)
def extract_data(path='fome_zero/data/zomato.csv'):
    return pd.read_csv(path)


# 2. Chama a função que extraiu o dataframe
def df_copy():
    df = extract_data
    df_raw = extract_data()

    # 3. Copia o dataframe original (df_raw) para o de trabalho (df)
    df = df_raw.copy()
    return df


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
        1: 'India',
        14: 'Australia',
        30: 'Brazil',
        37: 'Canada',
        94: 'Indonesia',
        148: 'New Zeland',
        162: 'Philippines',
        166: 'Qatar',
        184: 'Singapure',
        189: 'South Africa',
        191: 'Sri Lanka',
        208: 'Turkey',
        214: 'United Arab Emirates',
        215: 'England',
        216: 'United States of America'
    }
    return COUNTRIES[country_code]




