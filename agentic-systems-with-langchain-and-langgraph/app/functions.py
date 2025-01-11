import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def get_price_data(ticker, start, end):
    """
    Retorna um DataFrame com dados de preço (Adj Close) do ticker em yfinance.
    """
    df = yf.download(ticker, start=start, end=end, progress=False)
    if not df.empty:
        df = df[['Adj Close']].rename(columns={'Adj Close': ticker})
    return df

def get_dividend_data(ticker, start_date="2024-01-01", end_date="2025-01-01"):
    """
    Retorna um DataFrame com dados mensais do ticker (interval='1mo'),
    incluindo colunas de Data, Cotacao (Close), Dividends e Div%.

    - Div% = (Dividends / Cotacao) * 100
    """

    # 1. Baixa os dados mensais já agregados:
    data = ticker.history(
        start=start_date,
        end=end_date,
        interval='1mo'
    ).reset_index()

    # 2. Ajusta nome das colunas para ficar mais intuitivo
    data.rename(
        columns={
            "Date": "Data",
            "Close": "Cotacao",
            "Dividends": "Dividendos"
        },
        inplace=True
    )

    # 3. Calcula a % de dividendos em relação ao preço de fechamento
    #    Protege contra divisão por zero (caso Cotacao = 0)
    data["Div%"] = data.apply(
        lambda row: (row["Dividendos"] / row["Cotacao"] * 100) if row["Cotacao"] != 0 else 0,
        axis=1
    )

    # 4. Retorna apenas as colunas de interesse
    return data[["Data", "Cotacao", "Dividendos", "Div%"]]

def get_indices_data(start, end):
    """
    Retorna um DataFrame com (exemplo) IBOV (^BVSP), IFIX (IFIX.SA),
    IPCA e CDI de forma fictícia (para fins de exemplo).
    
    - IBOV e IFIX via yfinance
    - IPCA e CDI simulados (placeholders)
    """
    # IBOVESPA
    ibov = get_price_data('^BVSP', start, end)  # Índice do IBOV
    # IFIX
    ifix = get_price_data('IFIX.SA', start, end)  # Nem sempre funciona no yfinance
    
    # Exemplo fictício de IPCA mensal convertido para "curva de crescimento"
    # Supondo que cada mês tenha um valor de inflação e vamos montar cumulativo
    # Na prática, você poderia substituir por dados oficiais via API Bacen.
    datas = pd.date_range(start, end, freq='D')
    ipca_df = pd.DataFrame(index=datas, columns=['IPCA'])
    ipca_df['IPCA'] = 0.0
    # Simula uma inflação mensal, ex: ~0.5% ao mês
    for i in range(len(ipca_df)):
        ipca_df.iloc[i] = 1 + 0.005 * (i // 30)  # Cresce 0.5% a cada 30 dias
    # Converte em índice acumulado
    ipca_df = ipca_df.cumprod()
    
    # Exemplo fictício de CDI diário
    # Supondo ~0.4% ao mês => ~0.013% ao dia
    cdi_df = pd.DataFrame(index=datas, columns=['CDI'])
    cdi_df['CDI'] = 1 + 0.00013 * np.arange(len(cdi_df))
    cdi_df = cdi_df.cumprod()
    
    # Concatena todos
    full_df = pd.concat([ibov, ifix, ipca_df, cdi_df], axis=1)
    # Preenche possíveis NaNs (ex: IFIX pode não ter dado naquele dia)
    full_df.fillna(method='ffill', inplace=True)
    full_df.fillna(method='bfill', inplace=True)
    
    return full_df