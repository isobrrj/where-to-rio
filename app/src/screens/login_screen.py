import streamlit as st
from manager.auth_manager import AuthManager
from utils.screen_template import ScreenTemplate


class LoginScreen(ScreenTemplate):
    """
    Classe responsável por gerenciar a tela de login.
    """

    def __init__(self, cookie_manager):
        self.auth_manager = AuthManager()
        self.cookie_manager = cookie_manager

    def show_window(self):
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
