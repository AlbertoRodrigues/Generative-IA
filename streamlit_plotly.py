import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# =============================================================================
# EXEMPLO 1: Scatter Plot
# =============================================================================
def data_processing_scatter(df):
    # Supõe que 'df' tenha as colunas "x" e "y"
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        title="Scatter Plot",
        labels={"x": "X", "y": "Y"}
    )
    return fig

# =============================================================================
# EXEMPLO 2: Line Chart
# =============================================================================
def data_processing_line(df):
    # Supõe que 'df' tenha as colunas "x" e "y"
    fig = px.line(
        df, 
        x="x", 
        y="y", 
        title="Line Chart",
        labels={"x": "X", "y": "Y"}
    )
    return fig

# =============================================================================
# EXEMPLO 3: Bar Chart
# =============================================================================
def data_processing_bar(df):
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.bar(
        df, 
        x="category", 
        y="value", 
        title="Bar Chart",
        labels={"category": "Categoria", "value": "Valor"}
    )
    return fig

# =============================================================================
# EXEMPLO 4: Grouped Bar Chart (Barras Agrupadas) com Eixo de Tempo
# =============================================================================
def data_processing_grouped_bar(df):
    # Supõe que 'df' tenha as colunas "date", "value" e "subcategory"
    fig = px.bar(
        df,
        x="date",
        y="value",
        color="subcategory",
        barmode="group",
        title="Grouped Bar Chart",
        labels={"date": "Data (Ano-Mês)", "value": "Valor", "subcategory": "Subcategoria"}
    )
    fig.update_xaxes(tickformat="%Y-%m")
    return fig

# =============================================================================
# EXEMPLO 5: Stacked Bar Chart (Barras Empilhadas) com Eixo de Tempo
# =============================================================================
def data_processing_stacked_bar(df):
    # Supõe que 'df' tenha as colunas "date", "value" e "subcategory"
    fig = px.bar(
        df,
        x="date",
        y="value",
        color="subcategory",
        barmode="stack",
        title="Stacked Bar Chart",
        labels={"date": "Data (Ano-Mês)", "value": "Valor", "subcategory": "Subcategoria"}
    )
    fig.update_xaxes(tickformat="%Y-%m")
    return fig

# =============================================================================
# EXEMPLO 6: Pie Chart
# =============================================================================
def data_processing_pie(df):
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.pie(
        df, 
        names="category", 
        values="value", 
        title="Pie Chart"
    )
    return fig

# =============================================================================
# EXEMPLO 7: Sunburst Chart
# =============================================================================
def data_processing_sunburst(df):
    # Supõe que 'df' tenha as colunas "ids", "labels", "parents" e "value"
    fig = px.sunburst(
        df, 
        ids='ids', 
        names='labels', 
        parents='parents', 
        values='value', 
        title="Sunburst Chart"
    )
    return fig

# =============================================================================
# EXEMPLO 8: Treemap Chart
# =============================================================================
def data_processing_treemap(df):
    # Supõe que 'df' possua colunas que definem a hierarquia, por exemplo, "parent" e "category", e "value"
    fig = px.treemap(
        df, 
        path=['parent', 'category'], 
        values='value', 
        title="Treemap Chart"
    )
    return fig

# =============================================================================
# EXEMPLO 9: Histogram
# =============================================================================
def data_processing_histogram(df):
    # Supõe que 'df' tenha uma coluna "data" com valores numéricos
    fig = px.histogram(
        df, 
        x="data", 
        nbins=30, 
        title="Histogram"
    )
    return fig

# =============================================================================
# EXEMPLO 10: Box Plot
# =============================================================================
def data_processing_box(df):
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.box(
        df, 
        x="category", 
        y="value", 
        title="Box Plot",
        labels={"category": "Categoria", "value": "Valor"}
    )
    return fig

# =============================================================================
# EXEMPLO 11: Violin Plot
# =============================================================================
def data_processing_violin(df):
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.violin(
        df, 
        x="category", 
        y="value", 
        box=True,
        title="Violin Plot",
        labels={"category": "Categoria", "value": "Valor"}
    )
    return fig

# =============================================================================
# EXEMPLO 12: 3D Scatter Plot
# =============================================================================
def data_processing_scatter3d(df):
    # Supõe que 'df' tenha as colunas "x", "y", "z" e, opcionalmente, "value" para definir a cor
    fig = px.scatter_3d(
        df, 
        x="x", 
        y="y", 
        z="z", 
        color="value", 
        title="3D Scatter Plot",
        labels={"x": "X", "y": "Y", "z": "Z"}
    )
    return fig

# =============================================================================
# EXEMPLO 13: 3D Surface Plot
# =============================================================================
def data_processing_surface(df):
    # Supõe que 'df' contenha colunas "x", "y" e "z". Pivotamos os dados para formar uma matriz.
    x = sorted(df["x"].unique())
    y = sorted(df["y"].unique())
    z = df.pivot(index="y", columns="x", values="z").values
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title="3D Surface Plot")
    return fig

# =============================================================================
# EXEMPLO 14: Heatmap
# =============================================================================
def data_processing_heatmap(df):
    # Supõe que 'df' seja uma matriz ou DataFrame com valores numéricos
    fig = px.imshow(df, title="Heatmap")
    return fig

# =============================================================================
# EXEMPLO 15: Bubble Chart
# =============================================================================
def data_processing_bubble(df):
    # Supõe que 'df' tenha as colunas "x", "y", "size" e "color"
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        size="size", 
        color="color", 
        title="Bubble Chart", 
        size_max=30,
        labels={"x": "X", "y": "Y"}
    )
    return fig

# =============================================================================
# Bloco de Teste (para uso dentro do Streamlit)
# =============================================================================
if __name__ == "__main__":
    st.title("Testando Exemplos de Gráficos com Plotly")
    
    # Exemplo de teste para Scatter Plot
    st.header("Scatter Plot")
    df_scatter = pd.DataFrame({
        "x": np.random.randn(100),
        "y": np.random.randn(100)
    })
    st.plotly_chart(data_processing_scatter(df_scatter), use_container_width=True)
    
    # Exemplo de teste para Line Chart
    st.header("Line Chart")
    df_line = pd.DataFrame({
        "x": np.linspace(0, 10, 100),
        "y": np.sin(np.linspace(0, 10, 100))
    })
    st.plotly_chart(data_processing_line(df_line), use_container_width=True)
    
    # Exemplo de teste para Bar Chart
    st.header("Bar Chart")
    df_bar = pd.DataFrame({
        "category": ["A", "B", "C", "D"],
        "value": [4, 7, 1, 8]
    })
    st.plotly_chart(data_processing_bar(df_bar), use_container_width=True)
    
    # Exemplo de teste para Grouped Bar Chart com eixo de tempo
    st.header("Grouped Bar Chart")
    dates = pd.date_range(start="2020-01-01", periods=6, freq='MS')
    df_grouped = pd.DataFrame({
        "date": np.repeat(dates, 2),
        "value": np.random.randint(1, 20, 12),
        "subcategory": ["X", "Y"] * 6
    })
    st.plotly_chart(data_processing_grouped_bar(df_grouped), use_container_width=True)
    
    # Exemplo de teste para Stacked Bar Chart com eixo de tempo
    st.header("Stacked Bar Chart")
    st.plotly_chart(data_processing_stacked_bar(df_grouped), use_container_width=True)
    
    # Exemplo de teste para Pie Chart
    st.header("Pie Chart")
    df_pie = pd.DataFrame({
        "category": ["A", "B", "C", "D"],
        "value": [10, 20, 30, 40]
    })
    st.plotly_chart(data_processing_pie(df_pie), use_container_width=True)
    
    # Exemplo de teste para Sunburst Chart
    st.header("Sunburst Chart")
    df_sunburst = pd.DataFrame({
        "ids": ["A", "B", "C", "A1", "A2"],
        "labels": ["A", "B", "C", "A1", "A2"],
        "parents": ["", "", "", "A", "A"],
        "value": [10, 20, 30, 5, 5]
    })
    st.plotly_chart(data_processing_sunburst(df_sunburst), use_container_width=True)
    
    # Exemplo de teste para Treemap Chart
    st.header("Treemap Chart")
    df_treemap = pd.DataFrame({
        "parent": ["", "A", "A", "B", "B"],
        "category": ["A", "A1", "A2", "B1", "B2"],
        "value": [50, 20, 30, 15, 35]
    })
    st.plotly_chart(data_processing_treemap(df_treemap), use_container_width=True)
    
    # Exemplo de teste para Histogram
    st.header("Histogram")
    df_hist = pd.DataFrame({
        "data": np.random.randn(500)
    })
    st.plotly_chart(data_processing_histogram(df_hist), use_container_width=True)
    
    # Exemplo de teste para Box Plot
    st.header("Box Plot")
    df_box = pd.DataFrame({
        "category": np.repeat(["A", "B", "C"], 100),
        "value": np.concatenate([
            np.random.randn(100) + 5, 
            np.random.randn(100), 
            np.random.randn(100) - 5
        ])
    })
    st.plotly_chart(data_processing_box(df_box), use_container_width=True)
    
    # Exemplo de teste para Violin Plot
    st.header("Violin Plot")
    st.plotly_chart(data_processing_violin(df_box), use_container_width=True)
    
    # Exemplo de teste para 3D Scatter Plot
    st.header("3D Scatter Plot")
    df_scatter3d = pd.DataFrame({
        "x": np.random.randn(100),
        "y": np.random.randn(100),
        "z": np.random.randn(100),
        "value": np.random.randn(100)
    })
    st.plotly_chart(data_processing_scatter3d(df_scatter3d), use_container_width=True)
    
    # Exemplo de teste para 3D Surface Plot
    st.header("3D Surface Plot")
    x_vals = np.linspace(-5, 5, 50)
    y_vals = np.linspace(-5, 5, 50)
    x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)
    df_surface = pd.DataFrame({
        "x": x_mesh.flatten(),
        "y": y_mesh.flatten(),
        "z": np.sin(np.sqrt(x_mesh.flatten()**2 + y_mesh.flatten()**2))
    })
    st.plotly_chart(data_processing_surface(df_surface), use_container_width=True)
    
    # Exemplo de teste para Heatmap
    st.header("Heatmap")
    df_heat = pd.DataFrame(np.random.rand(10, 10), columns=[chr(i) for i in range(65, 75)])
    st.plotly_chart(data_processing_heatmap(df_heat), use_container_width=True)
    
    # Exemplo de teste para Bubble Chart
    st.header("Bubble Chart")
    df_bubble = pd.DataFrame({
        "x": np.random.rand(50),
        "y": np.random.rand(50),
        "size": np.random.rand(50) * 100,
        "color": np.random.rand(50)
    })
    st.plotly_chart(data_processing_bubble(df_bubble), use_container_width=True)
