# ------------------------------------------------------------------------------------------
# Importação de bibliotecas
# ------------------------------------------------------------------------------------------

from turtle import st
import folium
import utils as us
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import plotly.figure_factory as ff

from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


# ------------------------------------------------------------------------------------------
# Funções de leitura do dataframe
# ------------------------------------------------------------------------------------------
# caminho relativo (deploy)
def extract_data(path='data/zomato.csv'):
    return pd.read_csv(path)

# 2. Chama a função que extraiu o dataframe


def df_copy():
    df = extract_data
    df_raw = extract_data()

    # 3. Copia o dataframe original (df_raw) para o de trabalho (df)
    df = df_raw.copy()
    return df


# ------------------------------------------------------------------------------------------
# # Chama funções em util.py
# ------------------------------------------------------------------------------------------
# df_raw recebe função 'def extract_data' em utils
df_raw = extract_data()

# Copia o dataframe original (df_raw) para o de trabalho (df)
df = df_raw.copy()

# Função de limpeza
df = us.clean(df)

# Função que renomea a colunas
df = us.rename_columns(df)

# Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(us.country_name)

# Função que categoriza a comida peloa faixa de preço
df['price_type'] = df.loc[:, 'price_range'].apply(
    lambda x: us.create_price_tye(x))


# ------------------------------------------------------------------------------------------
# FUNÇÃO PARA PLOTAR MAPA
# ------------------------------------------------------------------------------------------
def geolocal(df):
    mapa = (df.loc[:,
                   ['country_code', 'city', 'latitude', 'longitude', 'restaurant_name', 'cuisines']]
            .groupby(['country_code', 'city', 'restaurant_name'])
            .value_counts()
            .reset_index()
            .sample(1000))

    mapa_coordenadas = folium.Map(
        location=[5.9658, -11.6016], zoom_start=2)

    agrupador = MarkerCluster().add_to(mapa_coordenadas)

    for index, location_info in mapa.iterrows():
        (folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                       popup=location_info[['country_code', 'city', 'restaurant_name', 'cuisines']])
            .add_to(agrupador))

    mapa_coordenadas.add_child(folium.LatLngPopup())
    folium_static(mapa_coordenadas, width=None)


# ------------------------------------------------------------------------------------------
# FUNÇÕES GRÁFICAS
# ------------------------------------------------------------------------------------------
# 1. Qual o nome do país que possui mais cidades registradas?
def country_city(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    cities = (df.groupby('country_code')['city']
              .nunique()
              .sort_values(ascending=False)
              .reset_index())

    # gráfico
    fig = px.bar(cities, x=cities['country_code'], y=cities['city'],
                 title='Quantidade de cidades registradas por país',
                 labels={'country_code': 'País', 'city': 'Qtde Cidades'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 2. Qual o nome do país que possui mais restaurantes registrados?
def country_restaurant(df):
    # Agrupa a quantidade de cidades por país usando o nome do país
    restaurant = (df.groupby('country_code')['restaurant_id']
                  .nunique()
                  .sort_values(ascending=False)
                  .reset_index())

    # gráfico
    fig = px.bar(restaurant, x=restaurant['country_code'], y=restaurant['restaurant_id'],
                 title='Quantidade de restaurantes registrados por país',
                 labels={'country_code': 'Países', 'restaurant_id': 'Qtde de restaurantes'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
def country_price_range(df):
    df_aux = (df.loc[df['price_range'] == 4, ['restaurant_id', 'country_code']]
                .groupby('country_code')
                .count()
                .sort_values('restaurant_id', ascending=False)
                .reset_index())
    return df_aux.iloc[0]['country_code']


# 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
def cuisines_quantity(df):
    cuisines_country = (df.loc[:, ['cuisines', 'country_code']]
                        .groupby('country_code')
                        .nunique()
                        .sort_values(by='cuisines', ascending=False)
                        .reset_index())

    fig = px.bar(cuisines_country, x=cuisines_country['country_code'], y=cuisines_country['cuisines'],
                 title='Países com maior variedade culinária',
                 labels={'country_code': 'Países', 'cuisines': 'Tipos de culinária'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
def country_rank(df):
    rank = (df.loc[:, ['country_code', 'votes']]
            .groupby('country_code')
            .sum()
            .sort_values(by='votes', ascending=False)
            .reset_index())

    fig = px.bar(rank,
                 x=rank['country_code'],
                 y=rank['votes'],
                 title='Países com mais avaliações',
                 labels={'country_code': 'Países', 'votes': 'Avaliações'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
def country_delivery(df):
    delivery = (df.loc[:, ['country_code', 'is_delivering_now']]
                .groupby('country_code')
                .count()
                .sort_values(by='is_delivering_now', ascending=False)
                .reset_index())

    fig = px.bar(delivery,
                 x=delivery['country_code'],
                 y=delivery['is_delivering_now'],
                 title='Países com mais restaurantes delivery',
                 labels={'country_code': 'Países', 'is_delivering_now': 'Restaurantes que fazem entrega'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
def country_booking(df):
    booking = (df.loc[:, ['country_code', 'has_table_booking']]
               .groupby('country_code')
               .sum()
               .sort_values(by='has_table_booking', ascending=False)
               .reset_index())

    fig = px.bar(booking,
                 x=booking['country_code'],
                 y=booking['has_table_booking'],
                 title='Países com mais restaurantes que aceitam reservas',
                 labels={'country_code': 'Países', 'has_table_booking': 'Restaurantes que aceitam reservas'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
def countries_median(df):
    media_rank = (df.loc[:, ['country_code', 'votes']]
                  .groupby('country_code')
                  .median()
                  .sort_values(by='votes', ascending=False)
                  .reset_index())

    fig = px.bar(media_rank,
                 x=media_rank['country_code'],
                 y=media_rank['votes'],
                 title='Países com mais avaliçãoes em média',
                 labels={'country_name': 'Países', 'votes': 'Media de avaliações'})
    fig.update_traces(texttemplate='%{y}')
    return fig


# 9. Qual o nome do país que possui, na média, a maior nota média registrada?
def pais_com_maior_nota_media(df):
    best_mean_rating = (df.loc[:, ['country_code', 'aggregate_rating']]
                        .groupby('country_code')
                        .mean()
                        .sort_values(by='aggregate_rating', ascending=False)
                        .reset_index())
    return best_mean_rating.iloc[0]['country_code']


# 10. Qual o nome do país que possui, na média, a menor nota média registrada?
def pais_com_menor_nota_media(df):
    under_mean_rating = (df.loc[:, ['country_code', 'aggregate_rating']]
                         .groupby('country_code')
                         .mean()
                         .round(3)
                         .sort_values(by='aggregate_rating', ascending=True)
                         .reset_index())
    return under_mean_rating.iloc[0]['country_code']


# Visão Cidades

def restaurantes_registrados(df):
    df_aux = (df.loc[:, ['city', 'country_code', 'restaurant_id']]
              .groupby(['city', 'country_code'])
              .count()
              .sort_values(by='restaurant_id', ascending=False)
              .reset_index())
    return df_aux.iloc[0]['city']


def media_maior_4(df):
    df_aux = (df.loc[df['aggregate_rating'] > 4, ['country_code', 'city', 'aggregate_rating']]
              .groupby(['country_code', 'city'])
              .count()
              .head(10)
              .sort_values(by='aggregate_rating', ascending=False)
              .reset_index())

    fig = px.bar(df_aux,
                 x='city',
                 y='aggregate_rating',
                 color='country_code',
                 color_discrete_sequence=px.colors.qualitative.G10,
                 title='Cidades com mais restaurantes com nota média acima de 4',
                 labels={'city': 'Cidade',
                 'aggregate_rating': 'Qtde de restaurantes'},
                 category_orders={'city':df_aux['city']}
                 )
    fig.update_traces(texttemplate='%{y}')

    return fig
