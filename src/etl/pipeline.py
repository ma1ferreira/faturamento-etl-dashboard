from src.etl.extract import extrair_dados
from src.etl.transform import validar_csv, limpeza_dados, criar_colunas

def pipeline(arquivo, colunas):

    df = extrair_dados(arquivo) #busca o arquivo CSV e transforma no dataframe com as colunas traduzidas para português
    df = validar_csv(df, colunas) #verifica se contem as colunas obrigatórias
    df = limpeza_dados(df) #corrige os tipos de dados e remove registros inválidos
    df = criar_colunas(df) #cria novas colunas "Ano", "Mês", "Margem de Lucro" e "Ticket Médio"
    return df

#e então podemos usar uma única função pipeline para processar um DataFrame pronto para análise em qualquer página do projeto.