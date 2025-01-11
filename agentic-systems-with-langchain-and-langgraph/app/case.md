Projeto: Assistente de Recomendação de Fundos Imobiliários do Brasil

Descrição Geral:
Crie um sistema inteligente que auxilia investidores a encontrar fundos imobiliários (FIIs) brasileiros adequados ao seu perfil. O assistente fará buscas, análises e recomendações baseadas em critérios como dividend yield, setor (logística, comercial, residencial), valor de mercado e volatilidade.
Etapas do Projeto:
1. Objetivos

    Recomendar FIIs alinhados aos objetivos financeiros do investidor.
    Fornecer análises detalhadas sobre os fundos, com gráficos e indicadores importantes.
    Permitir a personalização da pesquisa com filtros (e.g., setor, retorno esperado).

2. Estruturação do Sistema

Utilize o LangGraph para implementar os seguintes agentes:

    Agente Coletor de Dados: Extrai informações de fontes como B3, sites financeiros (Status Invest, Funds Explorer), e relatórios do mercado.
    Agente Analisador: Calcula métricas importantes (e.g., dividend yield, P/VP, liquidez diária).
    Agente de Perfil de Investidor: Avalia o perfil do usuário com base em perguntas simples e sugere filtros iniciais.
    Agente Recomendador: Retorna uma lista personalizada de fundos imobiliários, organizados por relevância.

3. Fluxo de Trabalho no LangGraph

    Entrada do Usuário:
    O usuário responde a perguntas como:
        “Qual é seu foco: renda mensal ou crescimento?”
        “Qual nível de risco está disposto a assumir?”
    Processamento dos Dados:
        O Agente Coletor de Dados busca os FIIs disponíveis no mercado.
        O Agente Analisador avalia as métricas com base nas preferências do usuário.
        O Agente Recomendador retorna uma lista de fundos imobiliários personalizados.
    Saída:
    Uma interface amigável apresenta os resultados em gráficos e tabelas.