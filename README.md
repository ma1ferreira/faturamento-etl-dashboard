Este projeto foi desenvolvido com o objetivo de revisar os conteúdos da matéria "Bases Computacionais da Ciência", aprofundar meus estudos nos princípios iniciais de estruturação de uma pipeline de dados (ETL) e explorar a biblioteca Streamlit para o desenvolvimento de dashboards para análise de dados com Python.

A aplicação processa um registro de vendas fictício e exibe um dashboard interativo. O código contém anotações que fiz ao longo do desenvolvimento para fixar conceitos novos.

### Modularização

1.  **`paths.py`**: Centraliza todos os caminhos do projeto para que o sistema rode em qualquer sistema operacional.
2.  **`extract.py`**: Responsável por ler os dados do CSV e traduzir colunas do inglês para o português.
3.  **`transform.py`**: Realiza a tipagem de dados, remove valore negativos e cria novas colunas úteis para a análise.
4.  **`load.py`**: Salva os dados processados no formato **Parquet**. Incluí uma lógica de timestamp para salvar versões diferentes do arquivo.
5.  **`pipeline.py`**: Orquestra todas as funções acima na ordem correta para que os dados saiam do estado bruto e chegue pronto ao dashboard

### Funcionalidades do Dashboard

- **KPIs**: Resumo visual de Receita Total, Volume de Vendas, Ticket Médio e Lucro.
- **Análise de Top Clientes e Produtos**: Tabelas e gráficos para identificação dos maiores geradores de receita.
- **Painel de Estatísticas**: Cálculos de Média, Mediana, Variância e Desvio Padrão para entender a distribuição das vendas.
- **Gráficos customizados**: O usuário pode alternar entre gráficos de barras ou linhas e escolher quais eixos (X e Y) deseja visualizar.

### Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas**: Manipulação de dados
- **Streamlit**: Interface web do dashboard
- **Matplotlib**: Visualizações gráficas
- **Pathlib**: Gestão dos caminhos dos arquivos

![sistema-faturamento](https://github.com/user-attachments/assets/d4d8eb13-1488-4835-b62b-4464f00ab902)

