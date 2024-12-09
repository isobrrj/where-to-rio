from database.sessionmanager import SessionManager
import streamlit as st
from database.models import User


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