import streamlit as st
from database.config import SessionLocal
from database.models import User

# Função para inserir usuário no banco
def add_user_to_db(name, email, age, gender):
    session = SessionLocal()  # Cria uma sessão para o banco
    new_user = User(name=name, email=email, age=age, gender=gender)
    session.add(new_user)
    try:
        session.commit()
        return True, f"Usuário {name} adicionado com sucesso!"
    except Exception as e:
        session.rollback()
        return False, f"Erro ao adicionar o usuário: {e}"
    finally:
        session.close()  # Fecha a sessão

def render_register():
    st.title("Cadastro de Usuário")

    # Formulário
    with st.form("user_registration_form"):
        name = st.text_input("Nome", max_chars=120)
        email = st.text_input("Email", max_chars=120)
        age = st.number_input("Idade", min_value=1, max_value=150, step=1)
        gender = st.selectbox("Gênero", ["M", "F", "O"], help="Escolha: M (Masculino), F (Feminino), O (Outro)")

        # Botão para enviar o formulário
        submitted = st.form_submit_button("Cadastrar")

    # Inserir dados no banco se o formulário for enviado
    if submitted:
        if not name or not email or not age or not gender:
            st.error("Por favor, preencha todos os campos.")
        else:
            success, message = add_user_to_db(name, email, age, gender)
            if success:
                st.success(message)
            else:
                st.error(message)

if __name__ == "__main__":
    render_register()
