compras_restaurante_contexto = """
Este conjunto de dados representa registros de compras em um restaurante fictício. 
Cada linha descreve uma transação individual, incluindo informações como data, hora, item comprado, quantidade, valor unitário, forma de pagamento, entre outros detalhes relevantes para análise de vendas.
O objetivo é permitir que se analise o comportamento de compra dos clientes, identificar itens mais vendidos, total de vendas por data, forma de pagamento mais utilizada, entre outras métricas de gestão de um restaurante.
"""

compras_restaurante_metadados = """
ID_Compra: Um identificador único para cada transação.
Data: Data em que a compra foi realizada (formato DD/MM/AAAA).
Hora: Hora em que a compra foi registrada (formato HH:MM).
Item: Nome do produto ou prato adquirido na compra.
Categoria: Classificação do item (por exemplo, bebida, prato principal, sobremesa).
Quantidade: Quantidade do item comprado.
Preco_Unitario: Preço unitário do item em Reais (R$).
Total_Compra: Valor total da compra específica em Reais (R$). (Pode ser a soma de múltiplos itens iguais ou a soma se houver mais de um item na mesma transação, mas neste dataset simplificado, consideramos apenas um item por linha.)
Cliente: Nome do cliente (pode ser um identificador ou nome fictício).
Forma_Pagamento: Forma utilizada para pagar a conta (dinheiro, cartão de crédito, cartão de débito, etc.).
"""


experimentos_quimicos_contexto = """
Este conjunto de dados representa registros de experimentos químicos realizados em um laboratório.
Cada linha contém informações sobre a data do experimento, substâncias utilizadas, condições experimentais 
(temperatura, pressão, etc.), produto formado e eficiência da reação. O objetivo é auxiliar em análises de 
otimização de processos químicos, correlação entre variáveis e previsibilidade de resultados.
"""

experimentos_quimicos_metadados = """
ID_Experimento: Identificador único para cada experimento.
Data: Data em que o experimento foi realizado (formato DD/MM/AAAA).
Substancia_1: Nome da primeira substância utilizada.
Substancia_2: Nome da segunda substância utilizada.
Temperatura_C: Temperatura em graus Celsius (°C) na qual o experimento foi conduzido.
Pressao_atm: Pressão atmosférica durante o experimento (em atm).
Tempo_Reacao_min: Tempo total da reação (em minutos).
Produto_Formado: Nome do produto químico formado.
Rendimento_%: Rendimento percentual da reação em relação ao esperado.
"""

indicadores_empresa_contexto = """
Este conjunto de dados representa indicadores de desempenho de uma empresa ao longo de diferentes períodos.
Os indicadores incluem informações financeiras, operacionais e estratégicas, como faturamento, lucro, despesas,
número de clientes e crescimento percentual. O objetivo é auxiliar na análise de performance da empresa, 
identificação de tendências e suporte à tomada de decisões estratégicas.
"""

indicadores_empresa_metadados = """
Periodo: Período de tempo analisado (mensal, trimestral, etc.).
Faturamento: Receita total da empresa no período, em Reais (R$).
Lucro: Lucro líquido obtido pela empresa no período, em Reais (R$).
Despesas: Total de despesas operacionais e administrativas no período, em Reais (R$).
Clientes: Número total de clientes ativos no período.
Crescimento_Percentual: Crescimento percentual do faturamento em relação ao período anterior (%).
Retorno_Sobre_Investimento (ROI): Indicador percentual que mede a eficiência do investimento realizado no período.
Market_Share: Participação de mercado da empresa no período (%).
"""

avaliacoes_filmes_contexto = """
Este conjunto de dados representa avaliações de filmes feitas por usuários de uma plataforma de streaming fictícia, 
semelhante à Netflix. Cada linha inclui informações sobre o filme avaliado, como título, gênero, ano de lançamento, 
duração, diretor e nota atribuída pelo usuário, variando de 1 a 10. 
O objetivo é facilitar análises sobre o desempenho dos filmes, preferências dos usuários e cálculos de métricas como o Net Promoter Score (NPS).
"""

avaliacoes_filmes_metadados = """
ID_Avaliacao: Um identificador único para cada avaliação.
Usuario: Identificador único do usuário que avaliou o filme.
Titulo: Título do filme avaliado.
Genero: Gênero do filme (ex.: Ação, Comédia, Drama, etc.).
Ano_Lancamento: Ano em que o filme foi lançado.
Duracao_Min: Duração do filme em minutos.
Diretor: Nome do diretor do filme.
Nota: Nota atribuída ao filme pelo usuário (de 1 a 10).
"""
