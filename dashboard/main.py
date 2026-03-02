import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from src.etl.pipeline import pipeline
from src.etl.load import salvar_parquet

#from src.etl.pipeline import pipeline traz para cá a função pipeline que executa todo o processo de ETL
#from src.etl.load import salvar_parquet traz para cá a função que salva o dataframe processado no formato .parquet na pasta DATA_PROCESSED

st.set_page_config(layout="wide")

#ligação com o arquivo de estilo CSS
with open(".streamlit/styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Sistema de Faturamento")

colunas_obrigatorias = [
    "ID", "Data", "ID Cliente", "Região", "Produto", "Categoria", 
    "Quantidade", "Preço Unitário", "Custo", "Método de Pagamento",
    "Dias para entrega", "Devolvido", "Avaliação", "Receita Total", "Lucro"
]

# sidebar #

st.sidebar.subheader("Upload CSV")

arquivo = st.sidebar.file_uploader(
    "",
    type=["csv"],
    label_visibility="collapsed"
)

if arquivo is not None: #is not None verificar se o arquivo foi enviado
    df = pipeline(arquivo, colunas_obrigatorias)
else:
    st.warning("Envie um arquivo CSV para iniciar.")
    st.stop()

# sidebar: filtros #

st.sidebar.header("Filtros")

#multiselect permite selecionar múltiplas opções, sorted ordena os meses, unique retorna os valores da coluna escolhida apenas uma vez
mes_filtro = st.sidebar.multiselect("Selecione o Mês", sorted(df["Mês"].unique())) 
cliente_filtro = st.sidebar.multiselect("Selecione o cliente", sorted(df["ID Cliente"].unique()))
produto_filtro = st.sidebar.multiselect("Selecione o produto", sorted(df["Produto"].unique()))

#cria uma cópia do dataframe original para aplicar os filtros sem alterar o dataframe original
#df_filtrado é utilizado para todas as análises e gráficos, ou seja, os filtros aplicados vão afetar todas as análises e gráficos da dashboard
df_filtrado = df.copy()

if mes_filtro:
    df_filtrado = df_filtrado[df_filtrado["Mês"].isin(mes_filtro)]

if cliente_filtro:
    df_filtrado = df_filtrado[df_filtrado["ID Cliente"].isin(cliente_filtro)]

if produto_filtro:
    df_filtrado = df_filtrado[df_filtrado["Produto"].isin(produto_filtro)]

############################################################################3####

# KPIs #

total_receita = df_filtrado["Receita Total"].sum()
total_vendas = len(df_filtrado)
ticket_medio = df_filtrado["Ticket Médio"].mean()
lucro_total = df_filtrado["Lucro"].sum()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Receita Total", f"R$ {total_receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
k2.metric("Total Vendas", total_vendas)
k3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
k4.metric("Lucro Total", f"R$ {lucro_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.divider()

#################################################################################

analise_top_clientes = (
    df_filtrado.groupby("ID Cliente")["Receita Total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    )

g1, espaco, g2 = st.columns([1, 0.2, 2])

with g1:
    st.markdown("**Top 10 Clientes**")
    
    st.dataframe(
        analise_top_clientes.style.format({"Receita Total": "R$ {:,.2f}",}, decimal=',', thousands='.'), hide_index=True
    )

with g2:

    receita_mes = (
        df_filtrado.groupby("Mês")["Receita Total"]
        .sum()
        .reset_index()
        .sort_values("Mês")
    )

    #figsize define o tamanho do gráfico
    #marker define o formato dos pontos no gráfico de linha
    #color define a cor dos elementos do gráfico
    #labelsize define o tamanho da fonte dos rótulos dos eixos
    #transparent=True deixa o fundo do gráfico transparente

    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.plot(receita_mes["Mês"], receita_mes["Receita Total"], marker="o", color="#ffffff")
    ax.set_title("Receita por mês", fontsize=10, color="#ffffff")
    ax.tick_params(colors="#ffffff", labelsize=8)
    st.pyplot(fig, transparent=True)

    top_produtos = (
        df_filtrado.groupby("Produto")["Receita Total"]
        .sum()
        .sort_values(ascending=False)
        .head(5) #head(5) pega os 5 primeiros registros do dataframe, ou seja, os 5 produtos mais lucrativos
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.bar(top_produtos["Produto"], top_produtos["Receita Total"], color="#ffffff", width=0.5)
    ax.set_xticklabels(top_produtos["Produto"]) #xticklabels define os rótulos do eixo x, nesse caso os nomes dos 5 produtos mais vendidos
    ax.set_title("Top 5 Produtos", fontsize=10, color="#ffffff")
    ax.tick_params(colors="#ffffff", labelsize=8)
    st.pyplot(fig, transparent=True)

st.divider()

#################################################################################

# análises #

#cada groupby agrupa os dados por cliente, produto ou mês, somando a receita total de cada grupo e ordenando do maior para o menor

analise_vendas_mes = (
    df_filtrado.groupby("Mês")["Receita Total"]
    .sum()
    .reset_index()
)

analise_produtos = (
    df_filtrado.groupby("Produto")["Receita Total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

analise_clientes = (
    df_filtrado.groupby("ID Cliente")["Receita Total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Total por Mês")
    st.dataframe(
        analise_vendas_mes.style.format({"Receita Total": "R$ {:,.2f}"}, decimal=',', thousands='.'), hide_index=True,
    )

with col2:
    st.subheader("Total por Produto")
    st.dataframe(
        analise_produtos.style.format({"Receita Total": "R$ {:,.2f}"}, decimal=',', thousands='.'), hide_index=True, height=280
    )

with col3:
    st.subheader("Total por Cliente")
    st.dataframe(
        analise_clientes.style.format({"Receita Total": "R$ {:,.2f}", "ID Cliente": "{:.0f}"}, decimal=',', thousands='.'), hide_index=True, height=280
    )

st.divider()
############################################################################3####

# estatiscas descritivas #

#estatísticas também mudam de acordo com os filtros aplicados

media_r = df_filtrado["Receita Total"].mean()
mediana_r = df_filtrado["Receita Total"].median()
variancia_r = df_filtrado["Receita Total"].var()
desvio_r = df_filtrado["Receita Total"].std()

media_q = df_filtrado["Quantidade"].mean()
mediana_q = df_filtrado["Quantidade"].median()
variancia_q = df_filtrado["Quantidade"].var()
desvio_q = df_filtrado["Quantidade"].std()

#função formata os números para o formato brasileiro, com vírgula como separador decimal e ponto como separador de milhares
#recebe um valor numérico padrão do Pandas, por exemplo 1234.56
#retorna uma string formatada no estilo brasileiro, por exemplo "1.234,56"
def formatar_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

espaco, col1, espaco, col2, espaco = st.columns([0.4, 1, 0.1, 1, 0.4])

with col1:
    with st.container(border=True):
        st.subheader("Receita Total")

        c1, espaco, c2 = st.columns([1, 0.8, 1])

        with c1:
            st.write(f"Média:")
            st.write(f"Mediana:")
            st.write(f"Variância:")
            st.write(f"Desvio padrão:")

        with c2:
           st.write(f"R$ {formatar_br(media_r)}")
           st.write(f"R$ {formatar_br(mediana_r)}")
           st.write(f"{formatar_br(variancia_r)}")
           st.write(f"{formatar_br(desvio_r)}")

with col2:
    with st.container(border=True):
        st.subheader("Quantidade Vendida")

        c1, espaco, c2 = st.columns([1, 0.8, 1])

        with c1:
            st.write(f"Média:")
            st.write(f"Mediana:")
            st.write(f"Variância:")
            st.write(f"Desvio padrão:")

        with c2:
            st.write(f"{formatar_br(media_q)}")
            st.write(f"{formatar_br(mediana_q)}")
            st.write(f"{formatar_br(variancia_q)}")
            st.write(f"{formatar_br(desvio_q)}")

st.divider()

############################################################################

# gráficos personalizados #

st.subheader("Visualizações Gráficas")

col_x = st.selectbox("Selecione eixo X", ["Mês", "Produto"])
col_y = st.selectbox("Selecione eixo Y", ["Receita Total", "Quantidade", "Lucro"])
grafico = st.selectbox("Tipo", ["Barras","Linha"])

fig, ax = plt.subplots()

# barras / astype converte os valores do índice para string para evitar problemas de formatação no gráfico, agrupado.index é o índice do dataframe agrupado, agrupado.values são os valores da coluna y do dataframe agrupado

if grafico == "Barras":
    agrupado = df_filtrado.groupby(col_x)[col_y].sum()
    ax.bar(agrupado.index.astype(str), agrupado.values, color="#ffffff", width=0.5)


# linha / agrupado.index é o índice do dataframe agrupado, agrupado.values são os valores da coluna y do dataframe agrupado

else:
    agrupado = df_filtrado.groupby(col_x)[col_y].sum()
    ax.plot(agrupado.index, agrupado.values, marker="o", color="#ffffff")

# títulos do gráficos e dos eixos

ax.set_title(f"{col_x} vs {col_y}", color="#ffffff", fontsize=10)
ax.set_xlabel(col_x, color="#ffffff")
ax.set_ylabel(col_y, color="#ffffff")
ax.tick_params(colors="#ffffff", labelsize=8)

st.pyplot(fig, transparent=True)