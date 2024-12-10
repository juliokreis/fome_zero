# import pandas as pd
# import numpy as np
import PIL.Image as imgpil
import streamlit as st


st.set_page_config(
    page_title='Home',
    page_icon='🏠',
    layout='wide',
    initial_sidebar_state='auto'
)

image = imgpil.open('logo_restaurant.png')
st.sidebar.image(image, use_column_width='auto')

# st.sidebar.markdown('# Restaurant World')
# st.sidebar.markdown('Encontre seu restaurante no mundo')
st.sidebar.markdown('''---''')
st.sidebar.markdown('''## Powered by Júlio Reis''')

# ------------------------------------------

st.write('## RESTAURANT WORLD')

st.markdown(
    '''
#### Essa página de análise foi construído para responder perguntas de negócio que auxiliarão restaurantes e clientes.

### Como utilizar?

Esse dashboard está dividido em:

### Indicadores Gerais
São apresentados indicadores gerais e um mapa com a localização dos 
restaurantes cadastrados.

Cada restaurante destaca três elementos:
* Preço médio dos pratos para dois.
* Tipo principal de comida oferecida pelo restaurante.
* Classificação.

### Paises
* Nesta página é feito uma segmentação por paises.

### Cidades
* Nesta página é feito uma segmentação por cidades.

### Cozinhas
* Nesta página é feito uma segmentação por cozinhas.

Abaixo estão os filtros:
* Países.
* Cidades
* Cozinhas
* Valor do prato para dois

No botão download é possivel baixar em pdf a base de dados com os filtros selecionados.


Deixe seu contato para suporte: telefoen e/ou e-mail

💻 eveloped by Júlio Reis

''')
