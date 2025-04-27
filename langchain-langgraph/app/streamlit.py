import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from functions import get_price_data, get_dividend_data, get_indices_data

st.title("Análise de Ativos e Comparação com Índices")

# Lista de ativos para seleção (exemplo fictício).
# Substitua pelos tickers que você deseja disponibilizar ao usuário.
lista_ativos = ["HGLG11.SA", "BTLG11.SA", "XPML11.SA", "HGBS11.SA"]

# Barra lateral para seleção do ativo e períodos
st.sidebar.header("Configurações")
ticker_selecionado = st.sidebar.selectbox("Selecione o ativo", lista_ativos)

# Datas default
start_date = st.sidebar.date_input("Data inicial", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("Data final", datetime.date.today())

# Obtém dados de cotação diária
st.subheader(f"Cotação diária - {ticker_selecionado}")
df_price = yf.download(ticker_selecionado, start=start_date, end=end_date, progress=False)

if df_price.empty:
    st.warning("Não foram encontrados dados para o período selecionado.")

# Reseta o índice para que a coluna de data fique explícita no DataFrame
df_price.reset_index(inplace=True)
df_price.columns = df_price.columns.get_level_values('Price')
df_price["Date"] = pd.to_datetime(df_price["Date"])

#df_price = df_price[
#    (df_price["Date"] >= pd.to_datetime(start_date)) & 
#    (df_price["Date"] <= pd.to_datetime(end_date))
#]


# Criação do gráfico interativo com Plotly
fig = px.line(
    df_price,
    x="Date",
    y="Close",
    title=f"Evolução de {ticker_selecionado}",
    labels={"Date": "Data", "Close": "Preço de Fechamento (R$)"},
    markers=True  # Adiciona marcadores nos pontos
)

# Customizações
fig.update_traces(
    line=dict(width=2, color="white"),            # Cor da linha
    marker=dict(size=8, color="cyan")      # Cor dos marcadores
)
fig.update_layout(
    title=dict(font=dict(size=16, color="white", family="Arial")),
    xaxis=dict(
        title_font=dict(size=12, color="white"),  # Títulos e rótulos em branco
        tickfont=dict(color="white"),            # Cor dos rótulos do eixo X
        gridcolor="gray"                         # Cor da grade
    ),
    yaxis=dict(
        title_font=dict(size=12, color="white"),
        tickfont=dict(color="white"),
        gridcolor="gray"
    ),
    plot_bgcolor="black",                         # Fundo do gráfico em preto
    paper_bgcolor="rgba(0,0,0,0)",                # Fundo da área em preto transparente
    hoverlabel=dict(font_color="black", bgcolor="lightgray"),  # Tooltip com fundo claro
    hovermode="x unified"                         # Tooltip ao passar o mouse
)

# Mostra o gráfico no Streamlit
st.plotly_chart(fig)
# Obtém dados de dividendos
st.subheader("Dividendos mensais")
ticker_obj = yf.Ticker(ticker_selecionado)
df_div = get_dividend_data(ticker_obj, start_date=start_date, end_date=end_date)

import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Exemplo de DataFrame fictício, só para ilustrar.
# Substitua pelo seu DataFrame 'df_div' com colunas 'Data', 'Dividendos' e 'Cotacao'.
# ------------------------------------------------------------------------------
# import numpy as np
# data = pd.date_range('2022-01-01', '2022-12-31', freq='MS')
# df_div = pd.DataFrame({
#     'Data': data,
#     'Dividendos': [0, 0.5, 0, 0, 1, 0, 0.75, 0, 0, 0, 0.3, 0],
#     'Cotacao':   [10, 10.5, 10.2, 10.4, 10.8, 10.0,  9.9, 9.8, 10, 10.3, 10.5, 10.7]
# })

import streamlit as st
import pandas as pd
import plotly.graph_objs as go

if df_div.empty:
    st.info("Este ativo não teve dividendos no período (ou não foram encontrados).")
else:
    # Passo 1: Criar a coluna AnoMes (Period - Mensal)
    df_div['AnoMes'] = df_div['Data'].dt.to_period('M')
    
    # Passo 2: Agrupar Dividendos (soma) e Cotacao (última do mês)
    df_div_mensal = (
        df_div.groupby('AnoMes')
              .agg({'Dividendos': 'sum', 'Cotacao': 'last'})
    )
    
    # Passo 3: Gerar um range mensal do menor até o maior mês
    todos_meses = pd.period_range(
        start=df_div['Data'].min().to_period('M'),
        end=df_div['Data'].max().to_period('M'),
        freq='M'
    )

    # Passo 4: Reindexar para ter todos os meses do intervalo
    df_div_mensal = df_div_mensal.reindex(todos_meses, fill_value=0)
    
    # Renomear o índice para ficar padronizado
    df_div_mensal.index.name = 'AnoMes'
    
    # (Opcional) Forward fill da Cotacao se quiser evitar zeros nos meses sem cotação
    df_div_mensal['Cotacao'] = (
        df_div_mensal['Cotacao']
        .replace(0, pd.NA)
        .ffill()
    )
    
    # Passo 5: Calcular Div%
    # Div% = (Dividendos / cotação do mês) * 100
    df_div_mensal['Div%'] = (df_div_mensal['Dividendos'] / df_div_mensal['Cotacao']) * 100
    
    # Passo 6: Preparar DataFrame para o gráfico
    df_div_mensal = df_div_mensal.reset_index()
    # Converter 'AnoMes' (Period) em string para exibir no eixo X
    df_div_mensal['AnoMes'] = df_div_mensal['AnoMes'].astype(str)

    # Passo 7: Criar o gráfico Plotly (apenas um eixo y)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_div_mensal['AnoMes'],
            y=df_div_mensal['Dividendos'],
            name='Dividendos (R$)',
            marker_color='royalblue',
            customdata=df_div_mensal['Div%'],  # para exibir Div% no hover
            hovertemplate=(
                "Período: %{x}<br>"
                "Dividendos: R$ %{y:.2f}<br>"
                "Div%%: %{customdata:.1f}%%"
                "<extra></extra>"
            )
        )
    )
    
    # Passo 8: Ajustar o eixo X para exibir TODOS os meses
    # Definimos type='category' e definimos os tickvals/ticktext como a lista completa de meses
    todos_os_meses_str = df_div_mensal['AnoMes'].unique().tolist()
    
    fig.update_layout(
        title='Dividendos por Período',
        xaxis=dict(
            title='Período (Ano-Mês)',
            type='category',
            tickmode='array',
            tickvals=todos_os_meses_str,
            ticktext=todos_os_meses_str,
            tickangle= -45,  # pode ajustar o ângulo se ficar muito apertado
        ),
        yaxis_title='Dividendos (R$)',
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
