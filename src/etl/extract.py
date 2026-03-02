import pandas as pd
from src.paths import DATA_RAW

#from src.paths import DATA_RAW traz para cá a pasta onde ficam os arquivos CSV originais("processamento-informacao/data/raw")

#função recebe um arquivo CSV, lê o conteúdo e traduz os nomes das colunas para português
#retorna um DataFrame com as colunas traduzidas
def extrair_dados(arquivo):

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

    df = df.rename(columns=traducao)
    return df