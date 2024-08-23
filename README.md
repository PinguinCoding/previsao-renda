# Projeto de Previsão de Renda
## Visão Geral
Este projeto tem como objetivo criar e avaliar modelos de regressão usando uma base de dados, com ênfase na exploração, processamento e análise dos dados. O projeto é dividido em duas partes principais:

- **Jupyter Notebook**: Exploração, limpeza, processamento dos dados e treinamento de modelos.
- **Aplicação Web com Streamlit**: Filtragem, análise e visualização interativa dos dados.

## Jupyter Notebook
No Jupyter Notebook, foram realizados os seguintes passos:

### Exploração de Dados:

Analisou-se a estrutura e o conteúdo da base de dados.
Relatórios foram gerados para extrair informações importantes.
A entropia das variáveis foi avaliada.

### Limpeza e Processamento de Dados:

Tratamento de valores ausentes, dados duplicados e outras questões de qualidade dos dados.
Processamento da base de dados para prepará-la para o treinamento dos modelos.

### Treinamento de Modelos:

Treinamento de dois modelos de regressão:
- **Árvore de Regressão com Pós-Podagem**
- **Random Forest Regressor**
  
Ambos os modelos alcançaram métricas de desempenho em torno de 50%. Propôs-se que o desempenho inferior pode ser devido ao tamanho reduzido da base de dados.

## Aplicação Web com Streamlit
Uma aplicação web baseada em Streamlit foi desenvolvida para fornecer análise e visualização interativa dos dados. A aplicação permite aos usuários:

- Fazer upload de arquivos CSV ou Excel para análise.
- Filtrar dados com base em uma variável numérica e classes categóricas selecionadas pelo usuário, resultando em um perfil de dados personalizado.
- Visualizar estatísticas como média, mediana e desvio padrão.
- Analisar a proporção de cada classe e sua entropia.
- Realizar análise baseada no tempo ajustando a janela temporal e selecionando quais variáveis numéricas exibir no gráfico.

### Tecnologias Utilizadas
- **Pandas**: Manipulação e análise de dados.
- **NumPy**: Computação numérica.
- **Seaborn**: Visualização de dados.
- **Matplotlib**: Criação de gráficos e diagramas.
- **Streamlit**: Desenvolvimento de aplicações web.
- **Jupyter Notebook**: Ambiente de computação interativa.

## Showcase

https://github.com/user-attachments/assets/73b59b87-782f-4758-83bc-e40a0b112dd2

