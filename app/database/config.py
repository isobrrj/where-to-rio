from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///whereto_DB.db"

# Cria o engine para o SQLite
engine = create_engine(DATABASE_URL)

# Sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
