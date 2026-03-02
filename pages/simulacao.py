import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.sidebar.subheader("Upload de novo arquivo CSV")

arquivo = st.sidebar.file_uploader(
    "Envie um CSV atualizado",
    type=["csv"], 
    label_visibility="collapsed")

colunas_obrigatorias = [
    "ID",
    "Data",
    "ID Cliente",
    "Região",
    "Produto",
    "Categoria",    
    "Quantidade",
    "Preço Unitário",
    "Custo",
    "Método de Pagamento",
    "Dias para entrega",
    "Devolvido",
    "Avaliação",
    "Receita Total",
    "Lucro"
]

def validar_csv(df):
    colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns] #col for col in colunas_obrigatorias percorre cada coluna e verifica se ela não está presente em df.columns, se não estiver, adiciona à lista colunas_faltando

    if colunas_faltando:
        st.error("Arquivo inválido! Colunas faltando: " + ", ".join(colunas_faltando))
        st.stop()

if arquivo is not None:
    df = pd.read_csv(arquivo)
    st.sidebar.success(f"Arquivo carregado: {arquivo.name}")
else:
    df = pd.read_csv("data/faturamento_dataset.csv")

traducao = {
    "invoice_id": "ID",
    "date": "Data",
    "customer_id": "ID Cliente",
    "region": "Região",
    "product": "Produto",
    "category": "Categoria",
    "quantity": "Quantidade",
    "unit_price": "Preço Unitário",
    "payment_method": "Método de Pagamento",
    "delivery_days": "Dias para entrega",
    "returned": "Devolvido",
    "satisfaction_score": "Avaliação",
    "total_revenue": "Receita Total",
    "cost": "Custo",
    "profit": "Lucro"
}

df.rename(columns={c: traducao[c] for c in df.columns if c in traducao}, inplace=True)
validar_csv(df)

df["Data"] = pd.to_datetime(df["Data"]) #converte a coluna "Data" para o tipo datetimes
df["Custo"] = pd.to_numeric(df["Custo"]) #converte a coluna "Custo" para o tipo numérico

df["Ano"] = df["Data"].dt.year #cria uma nova coluna "Ano" extraindo o Ano da coluna "Data"
df["Mês"] = df["Data"].dt.month #cria uma nova coluna "Mês" extraindo o Mês da coluna "Data"
df["Margem de Lucro"] = df["Lucro"] / df["Receita Total"] #cria uma nova coluna "Margem de Lucro"
df["Ticket Médio"] = df["Receita Total"] / df["Quantidade"] #cria uma nova coluna "Ticket Médio"


st.title("Simulação de Cenários de Receita")

# bloco de correlação #

st.write("Correlação entre variáveis numéricas, mostrando como elas se relacionam entre si e quais têm mais impacto na receita")

# selecionar apenas colunas numéricas
df_corr = df.select_dtypes(include=np.number)

# matriz de correlação
corr = df_corr.corr() #calculo da correlação entre as colunas numéricas do dataframe df_corr, resultando em uma matriz de correlação onde cada elemento representa a correlação entre duas variáveis numéricas.

st.subheader("Matriz de Correlação")
st.dataframe(corr.round(2)) #round(2) arredonda os valores da matriz para 2 casas decimais

# heatmap
st.subheader("Heatmap de Correlação")

fig, ax = plt.subplots()

fig.colorbar(ax.matshow(corr)) #matshow mostra a matriz de correlação como uma imagem

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))

ax.set_xticklabels(corr.columns, rotation=90)
ax.set_yticklabels(corr.columns)

st.pyplot(fig)

# valores da correlação variam de -1 a +1
# se qualidade × receita_total ≈ 1 → vendas aumentam receita
# se custo × margem de lucro < 0 → custo alto reduz margem
# se preço unitário × qualidade < 0 → preço alto diminui vendas

# ===============================================================================

# regressões #

x = df["Quantidade"].values
y = df["Receita Total"].values

media_x = x.mean()
media_y = y.mean()

# coeficiente angular
numerador = sum((x - media_x) * (y - media_y))
denominador = sum((x - media_x)**2)
beta1 = numerador / denominador

# intercepto
beta0 = media_y - beta1 * media_x

# previsões
y_pred = beta0 + beta1 * x

# cálculo R²
r2 = 1 - (sum((y - y_pred)**2) / sum((y - media_y)**2))

#==============================================================================

# simlações baseada na regressão linear #

# controles do usuário
col1, col2, col3 = st.columns(3)

with col1:
    nova_quantidade = st.number_input("Previsão  de produtos vendidos", 1, 10000, 20) #define quantas unidades do produto se espera vender

with col2:
    variacao = st.number_input("Variação aleatória (%)", 0, 100, 10) #define a variação aleatória em torno da quantidade prevista

with col3:
    n_simulacoes = st.number_input("Número de simulações", 10, 1000, 10) #define quantas simulações serão realizadas para gerar a distribuição de receitas previstas

# lista de resultados
resultados = []

for _ in range(n_simulacoes):
    ruido = np.random.uniform(-variacao/100, variacao/100) #gera um número aleatório entre -variacao% e +variacao%
    qtd_simulada = nova_quantidade * (1 + ruido) #adiciona 1 ao ruído para criar uma variação simulada da quantidade prevista
    receita_prevista = beta0 + beta1 * qtd_simulada # previsão usando regressão
    resultados.append(receita_prevista)

resultados = np.array(resultados)

media_sim = resultados.mean()
max_sim = resultados.max()
min_sim = resultados.min()

col1, col2, col3 = st.columns(3)

col1.metric("Receita média prevista", f"R$ {media_sim:,.2f}")
col2.metric("Melhor cenário", f"R$ {max_sim:,.2f}")
col3.metric("Pior cenário", f"R$ {min_sim:,.2f}")


# previsão da receita mensal real
receita_mensal = (
    df.groupby(["Ano","Mês"])["Receita Total"]
    .sum()
    .reset_index()
)

# criar eixo temporal numérico
receita_mensal["t"] = range(len(receita_mensal)) #range

# regressão linear temporal
x = receita_mensal["t"].values
y = receita_mensal["Receita Total"].values

b1 = sum((x-x.mean())*(y-y.mean())) / sum((x-x.mean())**2)
b0 = y.mean() - b1*x.mean()

# prever próximos meses
meses_prever = st.slider("Meses futuros para prever",1,12,3)

futuros = []
ultimo_t = x.max()

for i in range(1, meses_prever+1):
    t_futuro = ultimo_t + i
    receita_prevista = b0 + b1*t_futuro
    futuros.append(receita_prevista)

# dataframe previsão
df_prev = pd.DataFrame({
    "Mes_Futuro": range(1, meses_prever+1),
    "Receita Prevista": futuros
})

st.dataframe(df_prev)

# gráfico
fig, ax = plt.subplots()

ax.plot(receita_mensal["t"], y, marker="o", label="Real")
ax.plot(range(ultimo_t+1, ultimo_t+1+meses_prever), futuros, marker="o", linestyle="--", label="Previsto")

ax.set_title("Previsão de Receita")
ax.set_xlabel("Tempo")
ax.set_ylabel("Receita")
ax.legend()

st.pyplot(fig)
