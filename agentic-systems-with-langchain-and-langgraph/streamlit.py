import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

# ============================================================================
# Funções auxiliares
# ============================================================================

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

# ============================================================================
# Início do aplicativo Streamlit
# ============================================================================

def main():
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
        return
    
    st.dataframe(df_price[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10))
    
    # Obtém dados de dividendos
    st.subheader("Dividendos mensais")
    ticker_obj = yf.Ticker(ticker_selecionado)
    df_div = get_dividend_data(ticker_obj)
    
    if df_div.empty:
        st.info("Este ativo não teve dividendos no período (ou não foram encontrados).")
    else:
        # Exibe tabela de dividendos (com R$ e %)
        # Vamos agrupar por Ano/Mes para somar ao mês
        df_div['AnoMes'] = df_div['Data'].dt.to_period('M')
        df_div_mensal = df_div.groupby('AnoMes').agg({
            'Dividendos': 'sum',
            'Cotacao': 'last'
        })
        # Calcula a % no agregado mensal (soma dos dividendos no mês / cotação do final do mês)
        df_div_mensal['Div%'] = (df_div_mensal['Dividendos'] / df_div_mensal['Cotacao']) * 100
        st.dataframe(df_div_mensal)
    
    # Comparação do desempenho do ativo com IBOV, IPCA, IFIX, CDI
    st.subheader("Comparação de desempenho")
    # Obter dados de fechamento ajustado do ativo
    df_ativo = df_price[['Adj Close']].copy()
    df_ativo.rename(columns={'Adj Close': ticker_selecionado}, inplace=True)
    # Normaliza para base 1 (ou 100) para fazer comparação relativa
    df_ativo[ticker_selecionado] = df_ativo[ticker_selecionado] / df_ativo[ticker_selecionado].iloc[0]
    
    # Obtém índices
    df_indices = get_indices_data(start_date, end_date)
    # Precisamos mesclar com df_ativo
    df_compare = pd.concat([df_ativo, df_indices], axis=1)
    df_compare.fillna(method='ffill', inplace=True)
    df_compare.fillna(method='bfill', inplace=True)
    
    # Normaliza IBOV e IFIX também para 1 a partir da mesma data do ativo
    # (ou poderíamos ter normalizado cada um a partir de sua primeira data disponível)
    for col in ["^BVSP", "IFIX.SA"]:
        if col in df_compare.columns:
            df_compare[col] = df_compare[col] / df_compare[col].iloc[0]
    
    # IPCA e CDI são índices simulados (cumulativo de 1+algo), já estão "normalizados"
    # Se quiser deixar tudo começando em 1 no start_date, é possível ajustar também:
    for col in ["IPCA", "CDI"]:
        if col in df_compare.columns and df_compare[col].iloc[0] != 0:
            df_compare[col] = df_compare[col] / df_compare[col].iloc[0]
    
    # Exibe gráfico
    st.line_chart(df_compare, height=400)
    st.markdown("""
    **Observações:**
    - Os valores de IPCA e CDI aqui são **exemplos fictícios** (placeholders).
    - Caso queira dados reais, utilize APIs específicas do Bacen, IBGE ou consultoria de mercado.
    """)

if __name__ == "__main__":
    main()
