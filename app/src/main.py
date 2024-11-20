import streamlit as st
from utils.auth.auth_users import AuthUser
from request_screen import RequestScreen
from tourism_preference import TourismPreference

authenticator = AuthUser()

login_status = authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    request_screen = RequestScreen()
    init_date, end_date, neigh, preferences = request_screen.show_window()
    tourism_preference = TourismPreference(neigh=neigh,
                                            init_date=init_date,
                                            end_date=end_date,
                                            preferences=preferences)
    print(tourism_preference.build_message())

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')

