import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Obtém o diretório atual onde o arquivo config.py está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho absoluto para o banco de dados
DATABASE_PATH = os.path.join(BASE_DIR, "whereto_DB.db")

# URL do banco de dados SQLite
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Cria o engine para conectar ao banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configura a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
