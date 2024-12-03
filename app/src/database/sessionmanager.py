from database.config import SessionLocal

class SessionManager:
    """
    Implementa um Singleton para gerenciar a sessão do banco de dados.
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = SessionLocal()
        return cls._instance
