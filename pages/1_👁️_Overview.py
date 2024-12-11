import functions
import utils as us
import streamlit as st
import PIL.Image as imgpil

from streamlit_folium import folium_static
# ----------------------------------------------------------------
# 
# ----------------------------------------------------------------

st.set_page_config(
    page_title='Visão geral',
    page_icon='👁️',
    layout='wide',
    initial_sidebar_state='auto'
)

# ----------------------------------------------------------------
# Leitura do dataframe bruto
# ----------------------------------------------------------------
# 1.Função que lê o dataframe
df = us.extract_data()

# Função de limpeza
df = us.clean(df)

# 3.Função que renomea a colunas
df = us.rename_columns(df)

# 4.Função que gera o código ao nome de cada pais
df['country_code'] = df['country_code'].apply(us.country_name)

# ----------------------------------------------------------------
# Chamada das funções no util.py
# ----------------------------------------------------------------
# # 3.Função que renomea a colunas
# df = us.rename_columns(df)

# # 4.Função que gera o código ao nome de cada pais
# df['country_code'] = df['country_code'].apply(us.country_name)

# ------------------------------------------------------------------------------------------
# FUNÇÃO PARA PLOTAR MAPA
# ----------------------------------------------------------------
with st.container():
    # Chama a função 'def geolocal' para plotar o mapa
    st.markdown('## Distribuição dos restaurantes pelo mundo')
    geolocal = functions.geolocal(df)

# ------------------------------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------------------------------

image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# Filtro multiseletor de paises
st.markdown('### Escolha o país.')
country_options = (
    st.sidebar.multiselect
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
st.header('Overview')

st.markdown('Fale, resumidamente, sobre os dados que esta página mostra')

with st.container(border=True):   
    col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
    with col1:
        # 2. Quantos países únicos estão registrados
        paises = df['country_code'].nunique()
        col1.metric(':material/public: COUNTRIES', paises)
        
    with col1:
        # 3. Quantas cidades únicas estão registradas?
        cidades = df['city'].nunique()
        col1.metric(':material/location_city: CITIES', cidades)
            
    with col2:
        # 1. Quantos restaurantes únicos estão registrados?
        restaurantes = df['restaurant_id'].nunique()
        col2.metric(':material/restaurant: RESTAURANTS', restaurantes)
        
    with col2:
        # 5. Qual o total de tipos de culinária registrados?
        culinaria = df['cuisines'].nunique()
        col2.metric(':material/skillet_cooktop: CUISINES', culinaria)
        
    with col3:
        # 4. Qual o total de avaliações feitas?
        # (As avaliações são feitas pela quantidade de votos)
        avaliacoes = df['votes'].sum()
        col3.metric(':material/star_rate_half: RATING', avaliacoes)

    with col3:
        # 9. Qual o nome do país que possui, na média, a MAIOR nota média registrada?
        # (As avaliações são feitas pela quantidade de votos)
        best_average = functions.pais_com_maior_nota_media(df)
        col3.metric(':material/thumb_up: BEST RATED COUNTRY', best_average)

    with col4:
        # 3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
        # (As avaliações são feitas pela quantidade de votos)
        most_expensive = functions.country_price_range(df)
        col4.metric(':material/payments: COUNTRY EXPENSIVE RESTAURANT', most_expensive)

    with col4:
        # 10. Qual o nome do país que possui, na média, a menor nota média registrada?
        worst_average = functions.pais_com_menor_nota_media(df)
        col4.metric(':material/thumb_down: WORST RATED COUNTRY', worst_average)
        
    st.markdown(''' ---''')

