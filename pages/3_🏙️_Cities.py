import functions
import utils as us
import streamlit as st
import PIL.Image as imgpil
# import plotly.graph_objects as go
# import plotly.figure_factory as ff


# ----------------------------------------------------------------
# Configuração da page
# ----------------------------------------------------------------
# Este deve ser o primeiro comando Streamlit usado em uma página de aplicativo
# e deve ser definido apenas uma vez por página.
st.set_page_config(
    page_title='Países',
    page_icon='🏙️',
    layout='wide',
    initial_sidebar_state='auto'
)


# ----------------------------------------------------------------
# Chama funções em util.py
# ----------------------------------------------------------------
# 1.Função que lê o dataframe
df = us.extract_data()

# Função de limpeza
df = us.clean(df)

# Função que renomea a colunas
df = us.rename_columns(df)

# Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(us.country_name)

# Função que categoriza a comida peloa faixa de preço
df['price_type'] = df.loc[:, 'price_range'].apply(
    lambda x: us.create_price_tye(x))


# ----------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------
image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
st.markdown('### Escolha o país.')
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
                        'Qatar',
                        'Singapure',
                        'South Africa',
                        'Sri Lanka',
                        'Turkey',
                        'United Arab Emirates',
                        'England',
                        'USA'
                    ]
                   )
                  )
    
linhas_selecionadas = df['country_code'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')


# ----------------------------------------------------------------
# LAYOUT STREAMLIT
# ----------------------------------------------------------------
with st.container(border=True):
    st.markdown('Visão Cidades')
    st.markdown('''
                O objetido dessa análise é conhecer melhor os dados das cidades e encontrar padrões que 
                ofereçam percepções para melhorar a tomada de decisões estratégicas.
                ''')

with st.container(border=True):
    st.markdown('### City ​​Metrics')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Visão geral (Overview): 3. Quantas cidades únicas estão registradas?
        cidades = df['city'].nunique()
        col1.metric(':material/location_city: CITIES', cidades)

    with col1:
        # 1. Qual o nome da cidade que possui mais restaurantes registrados?
        registrados = functions.restaurantes_registrados(df)
        col1.metric(':material/location_city: CITIES', registrados)

    with col2:
        st.markdown(':material/app_registration: restaurantes cadastrados')

    with col3:
        st.markdown(':material/skillet_cooktop: variedade culinaria')

with st.container(border=True):
    st.markdown('### Gráficos')
    fig = functions.media_maior_4(df)
    st.plotly_chart(fig, use_container_width=True)
    
