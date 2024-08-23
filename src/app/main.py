import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


@st.cache_data
def load_data(file_pointer, op):
    try:
        if op == 'Excel':
            return pd.read_excel(file_pointer)
        else:
            if op == 'CSV (,)':
                return pd.read_csv(file_pointer, sep=',')
            else:
                return pd.read_csv(file_pointer, sep=';')
    except:
        raise TypeError('File Type not Accepted')


@st.cache_data
def calculate_entropy(tab_freq):
    h = 0
    for cls in tab_freq.index:
        h += tab_freq[cls] * np.log2(tab_freq[cls])
    return h * -1


@st.cache_data
def calculate_max_entropy(tab_freq):
    return np.log2(len(tab_freq))


@st.cache_data
def multiselect_filter(data, col, selected_cols):
    if 'all' in selected_cols:
        return data
    else:
        return data[data[col].isin(selected_cols)].reset_index(drop=True)


def main():
    global dataset

    st.set_page_config(
        page_title="Análise Exploratória",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.write('# Análise Exploratória da Previsão de Renda')

    st.write('Use a Barra Lateral para Iniciar')

    st.sidebar.write('# Carregue Base de Dados')
    op = st.sidebar.selectbox('Tipo do Arquivo', ('CSV (,)', 'CSV (;)', 'Excel'))
    fp = st.sidebar.file_uploader('Base de dados', type=['csv', 'xlsx'])

    st.write('---')
    st.sidebar.write('---')

    if fp is not None:
        dataset_raw = load_data(fp, op)
        dataset = dataset_raw.copy()

        st.write('### Base de Dados Bruta')
        st.write(dataset_raw.head())

        if 'selected_num_vars' not in st.session_state:
            st.session_state.selected_num_vars = []

        if 'selected_cat_vars' not in st.session_state:
            st.session_state.selected_cat_vars = []

        if 'selected_vars' not in st.session_state:
            st.session_state.selected_vars = []

        if 'selected_var' not in st.session_state:
            st.session_state.selected_var = None

        st.sidebar.write('# Filtro Base de Dados')

        selected_var = st.sidebar.selectbox('Escolha a variável do filtro',
                                            [col for col in dataset.select_dtypes(include=['int64', 'float64'])])

        with st.sidebar.form(key='filter'):
            slider_filter = st.slider(label=f'Filtro {selected_var}:',
                                      min_value=int(dataset[selected_var].min()),
                                      max_value=int(dataset[selected_var].max()),
                                      value=(int(dataset[selected_var].min()),
                                             int(dataset[selected_var].max())))

            mapping = dict()

            cat_columns = [col for col in dataset if dataset[col].dtype == 'O']
            st.write('### Colunas Categóricas')

            for col in cat_columns:
                mapping[f'{col}_list'] = dataset[col].unique().tolist()
                mapping[f'{col}_list'].append('all')
                mapping[f'{col}_selected'] = st.multiselect(col.capitalize(),
                                                            mapping[f'{col}_list'],
                                                            ['all'])

            dataset = dataset.query(f'{selected_var} >= @slider_filter[0] and {selected_var} <= @slider_filter[1]')

            for column in cat_columns:
                selected_value = mapping[f'{column}_selected']
                dataset = dataset.pipe(multiselect_filter,
                                       column,
                                       selected_value)

            submit_button = st.form_submit_button(label='Aplicar')

        st.write('### Base de Dados Filtrada')
        st.write(dataset.head())

        st.write('**OBS:** Todas as análises na barra lateral são aplicadas ao conjunto de dados filtrado')

        st.sidebar.write('---')
        st.sidebar.write('# Análise Variáveis Contínuas')

        selected_num_vars = st.sidebar.multiselect('Selecione a(s) variável(s) númerica(s)',
                                                   [col for col in dataset.select_dtypes(include=['int64', 'float64'])],
                                                   default=st.session_state.selected_num_vars)

        st.session_state.selected_num_vars = selected_num_vars

        if st.sidebar.button('Média'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].mean().rename('média').T)

        if st.sidebar.button('Mediana'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].median().rename('mediana').T)

        if st.sidebar.button('Desvio Padrão'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].std().rename('desvio padrão').T)

        if st.sidebar.button('Todos'):
            st.write('### Análise Variáveis Contínuas')
            st.write(dataset[selected_num_vars].agg(['mean', 'median', 'std']).T)

        st.sidebar.write('---')
        st.sidebar.write('# Análise Variáveis Categóricas')

        selected_cat_vars = st.sidebar.multiselect('Selecione a(s) variável(s) categóricas(s)',
                                                   [col for col in dataset.select_dtypes(include=['object'])],
                                                   default=st.session_state.selected_cat_vars)

        st.session_state.selected_cat_vars = selected_cat_vars

        if st.sidebar.button('Frequência'):
            st.write('### Análise Variáveis Categóricas')
            st.write(dataset[selected_cat_vars].value_counts().sort_values(ascending=False).rename('frequência') / len(
                dataset[selected_cat_vars]))
            st.write('**OBS:** o cálculo sempre é feito considerando o tamanho amostral do conjunto todo')
            st.write('Tamanho amostral', len(dataset[selected_cat_vars]))

        if st.sidebar.button('%'):
            st.write('### Análise Variáveis Categóricas')
            st.write(dataset[selected_cat_vars].value_counts().sort_values(ascending=False).rename('%') / len(
                dataset[selected_cat_vars]) * 100)
            st.write('**OBS:** o cálculo sempre é feito considerando o tamanho amostral do conjunto todo')
            st.write('Tamanho amostral', len(dataset[selected_cat_vars]))

        if st.sidebar.button('Entropia'):
            st.write('### Análise Variáveis Categóricas')
            h = [calculate_entropy(dataset[col].value_counts() / len(dataset[col])) for col in selected_cat_vars]
            h_max = [calculate_max_entropy(dataset[col].value_counts() / len(dataset[col])) for col in selected_cat_vars]
            tx_h = [(h[i] / h_max[i]) * 100 for i in range(len(h))]
            st.write(
                pd.DataFrame(
                    {'entropia': h,
                     'entropia_máx': h_max,
                     'taxa_entropia (%)': tx_h
                     }, index=selected_cat_vars
                )
            )

        st.sidebar.write('---')
        st.sidebar.write('# Análise Temporal')

        date = pd.Series([date.date() for date in pd.to_datetime(dataset['data_ref'])])

        min_date = min(date)
        max_date = max(date)

        date_slider = st.sidebar.slider('Filtro de Data',
                                        min_value=min_date,
                                        max_value=max_date,
                                        value=(min_date, max_date),
                                        format='MMM/Y'
                                        )

        selected_vars = st.sidebar.multiselect('Selecione a(s) variável(s) categóricas(s)',
                                               [col for col in dataset.select_dtypes(include=['int64', 'float64'])],
                                               default=st.session_state.selected_vars)

        filtered = date[(date >= date_slider[0]) & (date <= date_slider[1])]

        for var in selected_vars:
            sns.lineplot(x=filtered,
                         y=dataset[var])
            plt.xticks(rotation=90)

        if st.sidebar.button('Mostrar'):
            st.pyplot(plt)


if __name__ == '__main__':
    main()
