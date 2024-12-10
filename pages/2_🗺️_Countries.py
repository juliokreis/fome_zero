# ----------------------------------------------------------------
# import de bibliotecas
# ----------------------------------------------------------------
import functions
import utils as us
import streamlit as st
import PIL.Image as imgpil

# import folium
# import numpy as np
# import pandas as pd
# from folium import plugins
# import plotly.express as px
# from streamlit_folium import folium_static

# ------------------------------------------------------------------------------------------
# ícone da abada de navegação
# ------------------------------------------------------------------------------------------
st.set_page_config(
    page_title='Países',
    page_icon='🌐',
    layout='wide',
    initial_sidebar_state='auto'
)

# ------------------------------------------------------------------------------------------
# Chama funções em util.py
# ------------------------------------------------------------------------------------------
# # df_raw recebe função 'def extract_data' em utils
# df_raw = us.extract_data()

# 1.Função que lê o dataframe
df = us.extract_data()

# Função de limpeza
df = us.clean(df)

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
# ------------------------------------------------------------------------------------------
# # 1. Qual o nome do país que possui mais cidades registradas?
# def city_country(df):
#     # Agrupa a quantidade de cidades por país usando o nome do país
#     pais = df.groupby('country_code')['city'].nunique().sort_values(ascending=False).reset_index()

#     # gráfico
#     fig = px.bar(pais, x=pais['country_code'], y=pais['city']
#                  ,title='Quantidade de cidades por País'
#                  ,labels={'country_code': 'País', 'city': 'Qtde Cidades'})
#     fig.update_traces(texttemplate = '%{y}') 
#     return fig
    
# # 2. Qual o nome do país que possui mais restaurantes registrados?
# def restaurant_country(df):
#     # Agrupa a quantidade de cidades por país usando o nome do país
#     country=(df.groupby('country_code')['restaurant_id']
#             .nunique()
#             .sort_values(ascending=False)
#             .reset_index())

#     # gráfico
#     fig = px.bar(country, x=country['country_code'], y=country['restaurant_id'],
#                  title='Quantidade de cidades por País',
#                  labels={'country_code': 'País', 'restaurant_id': 'Qtde de restaurantes'})
#     fig.update_traces(texttemplate = '%{y}')
#     return fig


# # 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
# def level_price(df): 
#     level_price=(df.loc[df['price_range'] == 4, ['restaurant_id', 'country_code']]
#                  .groupby('country_code')
#                  .count()
#                  .sort_values('restaurant_id', ascending=False)
#                  .reset_index())
#     # gráfico
#     fig = px.bar(level_price, x=level_price['country_code'],y=level_price['restaurant_id'],
#                  title='Países com restaurantes nível 4',
#                  labels={'country_code': 'País', 'restaurant_id': 'Qtde restaurant gourmet'})
#     fig.update_traces(texttemplate = '%{y}')
#     return fig

# # 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
# def cuisines_quantity(df):
#     cuisines_country = (df.loc[:, ['cuisines', 'country_code']]
#                         .groupby('country_code')
#                         .nunique()
#                         .sort_values(by='cuisines', ascending=False)
#                         .reset_index())
    
#     fig = px.bar(cuisines_country, x=cuisines_country['country_code'], y=cuisines_country['cuisines'],
#                 title='Países com maior quantidade de tipos de culinária distintos',
#                 labels={'country_code': 'Países', 'cuisines': 'Tipos de culinária'})
#     fig.update_traces(texttemplate = '%{y}')
#     return fig

# # 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
# def country_rank(df):
#     rank = (df.loc[:, ['country_code', 'votes']]
#             .groupby('country_code')
#             .sum()
#             .sort_values(by='votes', ascending=False)
#             .reset_index())

#     fig = px.bar(rank, x=rank['country_code'], y=rank['votes'],
#                 title='Países com maior quantidade de avaliações feitas',
#                 labels={'country_code': 'Países', 'votes': 'Avaliações'})
#     fig.update_traces(texttemplate = '%{y}')
#     return fig

# # 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
# def country_delivery(df):
#     delivery = (df.loc[:, ['country_code', 'is_delivering_now']]
#                 .groupby('country_code')
#                 .count()
#                 .sort_values(by='is_delivering_now', ascending=False)
#                 .reset_index())
    
#     fig = px.bar(delivery, x=delivery['country_code'], y=delivery['is_delivering_now'],
#                 title='Países com maior quantidade de restaurantes que fazem entrega',
#                 labels={'country_code': 'Países', 'is_delivering_now': 'Restaurantes que fazem entrega'})
#     fig.update_traces(texttemplate = '%{y}')
#     return fig


# ------------------------------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------------------------------
image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
# st.sidebar.markdown('### Escolha o país.')
st.sidebar.markdown('''---''')

with st.sidebar.container():
    st.markdown('## COUNTRIES VIEW')

    country_options = (st.sidebar.multiselect
                       ('', sorted(set(df['country_code'].unique())),
                        default=[
                            'India',
                            'Australia',
                            'Brazil',
                            'Canada',
                            'Indonesia',
                            'New Zeland',
                            'Philippines',
                            'Qatar','Singapure',
                            'South Africa','Sri Lanka',
                            'Turkey',
                            'Emirates',
                            'England',
                            'USA'
                        ]
                       )
                      )
    
    linhas_selecionadas = df['country_code'].isin(country_options)
    df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')

# ------------------------------------------------------------------------------------------
# LAYOUT STREAMLIT
# ------------------------------------------------------------------------------------------

with st.container():
    # 1. Qual o nome do país que possui mais cidades registradas?
    # Chama a função 'def city_country' em functions para plotar o gráfico de barras
    fig = functions.country_city(df)
    st.plotly_chart(fig, use_container_width=True)

    # 2. Qual o nome do país que possui mais restaurantes registrados?
    # Chama a função 'def restaurant_country' em functions para plotar o gráfico de barras
    fig = functions.country_restaurant(df)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Chama a função 'def restaurant_country' para plotar o gráfico de barras
        fig = functions.cuisines_quantity(df)
        st.plotly_chart(fig, use_container_width=True)

        fig = functions.country_rank(df)
        st.plotly_chart(fig, use_container_width=True)

        # Chama a função 'country_booking' para plotar um gráfico de barras
        fig = functions.country_booking(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Chama a função 'def level_price' para plotar o gráfico de barras
        fig = functions.country_delivery(df)
        st.plotly_chart(fig, use_container_width=True)

        # cham a função countries_median para plotar o gráfico
        fig = functions.countries_median(df)
        st.plotly_chart(fig, use_container_width=True)
        # # Chama a função 'def level_price' para plotar o gráfico de barras
        # fig = level_price(df)
        # st.plotly_chart(fig, use_container_width=True)

        # # Chama a função 'def level_price' para plotar o gráfico de barras
        # fig = country_delivery(df)
        # st.plotly_chart(fig, use_container_width=True)


