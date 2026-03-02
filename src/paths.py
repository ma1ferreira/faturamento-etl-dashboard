from pathlib import Path

#com o pathlib dá para criar caminhos sem se as barras / ou \
#BASE_DIR é o diretório raiz do projeto = a pasta "processamento-informacao"
#DATA_RAW é o caminho para a pasta onde ficam os arquivos CSV originais = "processamento-informacao/data/raw"
#DATA_PROCESSED é o caminho para a pasta onde ficam os arquivos CSV processados = "processamento-informacao/data/processed"
#DB_PATH é o caminho para o arquivo do banco de dados SQLite = "processamento-informacao/database/faturamento.db"

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "database" / "faturamento.db"