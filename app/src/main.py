import streamlit as st
from utils.auth.auth_users import AuthUser
from request_screen import RequestScreen
from trip_guide_builder import TripGuideBuilder

authenticator = AuthUser()

login_status = authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    request_screen = RequestScreen()
    tourism_preference = request_screen.collect_tourism_preference()
    if tourism_preference:
        trip_guide_buider = TripGuideBuilder(tourism_preference=tourism_preference)
        st.write(trip_guide_buider.build_question_message_llm())

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')

