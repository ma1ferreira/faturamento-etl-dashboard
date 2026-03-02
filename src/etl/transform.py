import pandas as pd
from src.etl.extract import extrair_dados

#from src.etl.extract import extrair_dados traz para cá a função que lê o arquivo CSV e traduz os nomes das colunas para português

#validar_csv verifica se o DataFrame contém as colunas obrigatórias
#o "raise" levanta um erro informando quais colunas estão faltando
#retorna o DataFrame original se todas as colunas estiverem presentes
def validar_csv(df, colunas_obrigatorias):
    faltando = [c for c in colunas_obrigatorias if c not in df.columns]

    if faltando:
        raise ValueError(f"Colunas faltando: {faltando}")

    return df

#limpeza_dados converte a coluna "Data" para o tipo datetimes, a coluna "Custo" para o tipo numérico e filtra os registros da coluna "Quantidade" e "Preço Unitário" para valores acima de zero
#retorna o DataFrame com os tipos de dados corrigidos e os registros inválidos removidos
def limpeza_dados(df):
    df["Data"] = pd.to_datetime(df["Data"])
    df["Custo"] = pd.to_numeric(df["Custo"])
    df = df[df["Quantidade"] > 0]
    df = df[df["Preço Unitário"] > 0]
    return df

#criar_colunas cria novas colunas "Ano", "Mês", "Margem de Lucro" e "Ticket Médio" a partir das colunas existentes
#retorna o DataFrame com as novas colunas criadas
def criar_colunas(df):
    df["Ano"] = df["Data"].dt.year #cria uma nova coluna "Ano" extraindo o Ano da coluna "Data"
    df["Mês"] = df["Data"].dt.month #cria uma nova coluna "Mês" extraindo o Mês da coluna "Data"
    df["Margem de Lucro"] = df["Lucro"] / df["Receita Total"] #cria uma nova coluna "Margem de Lucro"
    df["Ticket Médio"] = df["Receita Total"] / df["Quantidade"] #cria uma nova coluna "Ticket Médio"
    return df