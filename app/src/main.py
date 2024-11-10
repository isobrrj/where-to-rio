import streamlit as st
from utils.auth.auth_users import AuthUser


authenticator = AuthUser()

login_status = authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    st.title('Página de Sistema')

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')

