import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def load_data(file_pointer, tipo):
    if tipo == 'Excel':
        return pd.read_excel(file_pointer)
    else:
        if tipo == 'CSV (,)':
            return pd.read_csv(file_pointer, sep=',')
        else:
            return pd.read_csv(file_pointer, sep=';')


def calcular_entropia(tab_freq):
    h = 0
    for classe in tab_freq.index:
        h += tab_freq[classe] * np.log2(tab_freq[classe])
    return h * -1


def calcular_entropia_maxima(tab_freq):
    return np.log2(len(tab_freq))


def main():
    global dataset

    st.set_page_config(
        page_title="Análise Exploratória",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.write('# Análise Exploratória da Previsão de Renda')

    renda = pd.read_csv('data/raw/previsao_de_renda.csv')

    st.write('Use a Barra Lateral para Iniciar')

    st.sidebar.write('# Carregue Base de Dados')
    sep = st.sidebar.selectbox('Tipo do Arquivo', ('CSV (,)', 'CSV (;)', 'Excel'))
    fp = st.sidebar.file_uploader('Bank marketing data', type=['csv', 'xlsx'])

    if fp is not None:
        dataset_raw = load_data(fp, sep)
        dataset = dataset_raw.copy()

        st.write('### Base de Dados Bruta')
        st.write(dataset_raw.head())

        if 'selected_num_vars' not in st.session_state:
            st.session_state.selected_num_vars = []

        if 'selected_cat_vars' not in st.session_state:
            st.session_state.selected_cat_vars = []

        st.sidebar.write('---')
        st.sidebar.write('# Análise Variáveis Contínuas')

        selected_num_vars = st.sidebar.multiselect('Selecione a(s) variável(s) númerica(s)',
                                                   [col for col in dataset.select_dtypes(include=['int64', 'float64'])],
                                                   default=st.session_state.selected_num_vars)

        st.session_state.selected_num_vars = selected_num_vars

        if st.sidebar.button('Média'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].mean().rename('média'))

        if st.sidebar.button('Mediana'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].median().rename('mediana'))

        if st.sidebar.button('Desvio Padrão'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].std().rename('desvio padrão'))

        if st.sidebar.button('Todos'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].agg(['mean', 'median', 'std']))

        st.sidebar.write('---')
        st.sidebar.write('# Análise Variáveis Categóricas')

        selected_cat_vars = st.sidebar.multiselect('Selecione a(s) variável(s) categóricas(s)',
                                                   [col for col in dataset.select_dtypes(include=['object', 'bool'])],
                                                   default=st.session_state.selected_cat_vars)

        st.session_state.selected_cat_vars = selected_cat_vars

        if st.sidebar.button('Frequência'):
            st.write('### Análise Variáveis Categóricas')
            st.write(dataset[selected_cat_vars].value_counts().rename('frequência') / len(dataset[selected_cat_vars]))

        if st.sidebar.button('%'):
            st.write('### Análise Variáveis Categóricas')
            st.write(dataset[selected_cat_vars].value_counts().rename('%') / len(dataset[selected_cat_vars]) * 100)

        if st.sidebar.button('Entropia'):
            st.write('### Análise Variáveis Categóricas')

            st.write(
                pd.Series(
                    {'entropia': calcular_entropia([dataset[col].value_counts() / len(dataset[col]) for col in dataset[selected_cat_vars]][0]),
                     'entropia_máx': calcular_entropia_maxima([dataset[col].value_counts() / len(dataset[col]) for col in dataset[selected_cat_vars]][0])
                     }
                )
            )

        # Make support multiple variables


if __name__ == '__main__':
    main()
