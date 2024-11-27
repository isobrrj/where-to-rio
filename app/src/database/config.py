from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///whereto_DB.db"

# Cria o engine para conectar ao banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configura a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
