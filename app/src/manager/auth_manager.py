from database.sessionmanager import SessionManager
from database.models import User
from hashlib import sha256
import streamlit as st


class AuthManager:
    """
    Classe responsável por gerenciar a autenticação de usuários.
    """

    def __init__(self):
        self.session = SessionManager()

    def hash_password(self, password):
        """
        Gera um hash SHA256 da senha.
        """
        return sha256(password.encode()).hexdigest()

    def authenticate_user(self, email, password):
        """
        Verifica as credenciais do usuário no banco de dados.
        """
        hashed_password = self.hash_password(password)
        try:
            user = self.session.query(User).filter(User.email == email, User.password == hashed_password).first()
            return user
        finally:
            self.session.close()
    
    @staticmethod
    def logout(cookie_manager):
        """
        Realiza o logout do usuário, limpando cookies e estado de sessão.
        """
        # Limpa o estado de sessão
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["user_name"] = "Visitante"
        
        # Limpa os cookies, garantindo que os valores sejam strings
        cookie_manager["logged_in"] = "false"
        cookie_manager["user_id"] = ""
        cookie_manager["user_name"] = ""
        cookie_manager.save()  # Atualiza os cookies no navegador
        st.rerun()