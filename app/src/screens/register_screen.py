import streamlit as st
from utils.screen_template import ScreenTemplate
from manager.user_manager import UserManager
import logging
logging.basicConfig(level=logging.DEBUG)


class RegisterScreen(ScreenTemplate):
    """
    Classe responsável por gerenciar a tela de cadastro.
    """

    def __init__(self):
        self.user_manager = UserManager()

    def show_window(self):
        """
        Renderiza o formulário de cadastro.
        """
        st.title("Cadastro de Usuário")

        # Formulário para inserir os dados
        with st.form("user_registration_form"):
            name = st.text_input("Nome", max_chars=120)
            email = st.text_input("Email", max_chars=120)
            password = st.text_input("Senha", type="password")
            age = st.number_input("Idade", min_value=1, max_value=150, step=1)
            gender = st.selectbox("Gênero", ["M", "F", "O"], help="Escolha: M (Masculino), F (Feminino), O (Outro)")
            submitted = st.form_submit_button("Cadastrar")

        # Inserir os dados no banco se o formulário for enviado
        if submitted:
            if not name or not email or not age or not gender:
                st.error("Por favor, preencha todos os campos.")
            else:
                success, message = self.user_manager.add_user(name ,password, email, age, gender)
                if success:
                    st.success(message)
                else:
                    st.error(message)