import pathlib as Path
import pandas as pd
from datetime import datetime
from src.paths import DATA_PROCESSED

#from src.paths import DATA_PROCESSED traz para cá os arquivos CSV processados("processamento-informacao/data/processed")

#salvar_parquet recebe um dataframe, um nome base "dataset"
#o nome do arquivo será "dataset" + timestamp da data e hora atual para garantir que cada arquivo salvo seja único
#o arquivo é salvo no formato .parquet na pasta DATA_PROCESSED
def salvar_parquet(df, nome_base="dataset"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{nome_base}_{timestamp}.parquet"

    caminho = DATA_PROCESSED / nome_arquivo
    df.to_parquet(caminho, index=False) #salva o DataFrame no formato .parquet, index=False para não salvar o índice do DataFrame como uma coluna no arquivo
    return caminho