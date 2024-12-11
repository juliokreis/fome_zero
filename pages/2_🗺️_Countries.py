# ------------------------------------------------------------------------------------------
# import de bibliotecas
# ------------------------------------------------------------------------------------------
import functions
import utils as us
import streamlit as st
import PIL.Image as imgpil

# ------------------------------------------------------------------------------------------
# ícone da abada de navegação
# ------------------------------------------------------------------------------------------
st.set_page_config(page_title='Países',
                   page_icon='🗺️',
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
 
