import streamlit as st
from utils.auth.auth_users import AuthUser
from utils.pages import Pages

authenticator = AuthUser()
login_status = authenticator.login()

pages = Pages()

if st.session_state["authentication_status"]:
    authenticator.logout()
    pages.page_flow()

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha inválido')

elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')

