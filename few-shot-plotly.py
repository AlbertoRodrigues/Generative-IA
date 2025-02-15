prompt = r'''Você é um gerador de código Python especializado em visualizações com Plotly. 
Sua tarefa é criar uma função chamada `data_processing` que recebe um DataFrame `df` e retorna um gráfico Plotly (objeto figura) de acordo com os inputs fornecidos. 
Os inputs serão:

1. **Pergunta de interesse:** Um enunciado que descreve o objetivo da análise ou o tipo de gráfico desejado.
2. **Metadados da base:** Informações sobre as colunas disponíveis, seus tipos e significados.
3. **Exemplos de valores de cada coluna:** Alguns exemplos de valores para ajudar a entender a estrutura dos dados.
4. **Base filtrada:** O DataFrame com os dados já filtrados conforme o contexto da pergunta.

Use os exemplos a seguir como referência para gerar a função desejada. 
Cada exemplo é uma função `data_processing` que recebe um DataFrame `df` e retorna um gráfico Plotly correspondente ao tipo de visualização indicado.

––––––– EXEMPLOS FEW-SHOT ––––––––––––––––––––––––––––––––––––––––––––

Exemplo 1: Scatter Plot
def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha as colunas "x" e "y"
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        title="Scatter Plot",
        labels={"x": "X", "y": "Y"}
    )
    return fig

Descrição: Cria um gráfico de dispersão usando as colunas "x" e "y".

Exemplo 2: Line Chart

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha as colunas "x" e "y"
    fig = px.line(
        df, 
        x="x", 
        y="y", 
        title="Line Chart",
        labels={"x": "X", "y": "Y"}
    )
    return fig

Descrição: Cria um gráfico de linha utilizando as colunas "x" e "y".

Exemplo 3: Bar Chart

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.bar(
        df, 
        x="category", 
        y="value", 
        title="Bar Chart",
        labels={"category": "Categoria", "value": "Valor"}
    )
    return fig

Descrição: Cria um gráfico de barras simples para comparar os valores de diferentes categorias.

Exemplo 4: Grouped Bar Chart (Barras Agrupadas) com Eixo de Tempo

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um gráfico de barras agrupadas (lado a lado) com o eixo X representando datas no formato "Ano-Mês".

Exemplo 5: Stacked Bar Chart (Barras Empilhadas) com Eixo de Tempo

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um gráfico de barras empilhadas com o eixo X representando datas.

Exemplo 6: Pie Chart

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.pie(
        df, 
        names="category", 
        values="value", 
        title="Pie Chart"
    )
    return fig

Descrição: Cria um gráfico de pizza para visualizar a distribuição percentual entre categorias.

Exemplo 7: Sunburst Chart

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um gráfico Sunburst para visualizar dados hierárquicos.

Exemplo 8: Treemap Chart

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' possua colunas que definem a hierarquia, por exemplo, "parent" e "category", e "value"
    fig = px.treemap(
        df, 
        path=['parent', 'category'], 
        values='value', 
        title="Treemap Chart"
    )
    return fig

Descrição: Cria um Treemap para visualizar a hierarquia dos dados.

Exemplo 9: Histogram

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha uma coluna "data" com valores numéricos
    fig = px.histogram(
        df, 
        x="data", 
        nbins=30, 
        title="Histogram"
    )
    return fig

Descrição: Cria um histograma para visualizar a distribuição dos dados.

Exemplo 10: Box Plot

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' tenha as colunas "category" e "value"
    fig = px.box(
        df, 
        x="category", 
        y="value", 
        title="Box Plot",
        labels={"category": "Categoria", "value": "Valor"}
    )
    return fig

Descrição: Cria um box plot para visualizar a distribuição estatística dos dados por categoria.

Exemplo 11: Violin Plot

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um violin plot combinando a densidade dos dados e um box plot interno.

Exemplo 12: 3D Scatter Plot

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um gráfico de dispersão 3D para visualizar dados em três dimensões.

Exemplo 13: 3D Surface Plot

def data_processing(df):
    import plotly.graph_objects as go
    # Supõe que 'df' contenha colunas "x", "y" e "z". Pivotamos os dados para formar uma matriz.
    x = sorted(df["x"].unique())
    y = sorted(df["y"].unique())
    z = df.pivot(index="y", columns="x", values="z").values
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title="3D Surface Plot")
    return fig

Descrição: Cria um gráfico de superfície 3D a partir dos dados fornecidos.

Exemplo 14: Heatmap

def data_processing(df):
    import plotly.express as px
    # Supõe que 'df' seja uma matriz ou DataFrame com valores numéricos
    fig = px.imshow(df, title="Heatmap")
    return fig

Descrição: Cria um heatmap que representa os valores de uma matriz por meio de uma escala de cores.

Exemplo 15: Bubble Chart

def data_processing(df):
    import plotly.express as px
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

Descrição: Cria um gráfico de bolhas onde o tamanho dos pontos representa uma dimensão adicional dos dados.

––––––– FIM DOS EXEMPLOS ––––––––––––––––––––––––––––––––––––––––––––

Instruções Finais:

    Analise a pergunta de interesse, os metadados e os exemplos de valores fornecidos para entender qual gráfico é mais apropriado.
    Utilize os exemplos acima como referência para estruturar o código.
    Gere a função data_processing que receba o DataFrame filtrado (df) e retorne o gráfico Plotly adequado ao contexto.

Gere somente a função data_processing conforme especificado, sem código adicional de Streamlit ou outras instruções de execução.

Obrigado!'''