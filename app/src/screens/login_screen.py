import streamlit as st
from database.sessionmanager import SessionManager
from database.models import User
from hashlib import sha256
from streamlit_cookies_manager import EncryptedCookieManager

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

class LoginScreen:
    """
    Classe responsável por gerenciar a tela de login.
    """

    def __init__(self, cookie_manager):
        self.auth_manager = AuthManager()
        self.cookie_manager = cookie_manager

    def render(self):
        """
        Renderiza o formulário de login.
        """
        st.title("Login")

        # Formulário de login
        with st.form("login_form"):
            email = st.text_input("Email", max_chars=120)
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar")

        # Processa o formulário
        if submitted:
            if not email or not password:
                st.error("Por favor, preencha todos os campos.")
            else:
                user = self.auth_manager.authenticate_user(email, password)
                if user:
                    st.success(f"Bem-vindo, {user.name}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user.user_id
                    st.session_state["user_name"] = user.name
                    # Salvar nos cookies
                    self.cookie_manager["logged_in"] = "true"
                    self.cookie_manager["user_id"] = str(user.user_id)
                    self.cookie_manager["user_name"] = user.name
                    self.cookie_manager.save()  # Salva os cookies no navegador
                    st.markdown(
                        """
                        <script>
                            setTimeout(function() {
                                window.location.reload();
                            }, 1000);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Credenciais inválidas. Por favor, tente novamente.")
