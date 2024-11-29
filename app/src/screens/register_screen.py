from database.sessionmanager import SessionManager
import streamlit as st
from database.models import User
import logging
from .home_screen import HomeScreen
logging.basicConfig(level=logging.DEBUG)

class UserManager:
    """
    Classe responsável por gerenciar usuários no banco de dados.
    """

    def __init__(self):
        self.session = SessionManager()

    def is_email_registered(self, email):
        """
        Verifica se o e-mail já está registrado.
        """
        try:
            user = self.session.query(User).filter(User.email == email).first()
            return user is not None
        finally:
            self.session.close()

    def add_user(self, name, password, email, age, gender):
        """
        Adiciona um novo usuário ao banco de dados.
        """
        if self.is_email_registered(email):
            return False, "Este e-mail já está cadastrado."

        new_user = User(name=name,password=password, email=email, age=age, gender=gender)
        self.session.add(new_user)
        try:
            self.session.commit()
            return True, f"Usuário {name} adicionado com sucesso!"
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erro ao adicionar o usuário: {e}")
            return False, f"Erro ao adicionar o usuário: {e}"
        finally:
            self.session.close()


class RegisterScreen:
    """
    Classe responsável por gerenciar a tela de cadastro.
    """

    def __init__(self):
        self.user_manager = UserManager()

    def render(self):
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