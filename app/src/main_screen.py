import streamlit as st
from screens.home_screen import HomeScreen
from screens.base_screen import BaseScreen
from screens.response_screen import ResponseScreen
from screens.register_screen import RegisterScreen
from screens.login_screen import LoginScreen
from tripguide.test_trip_guide import trip

# Configuração inicial da página
st.set_page_config(page_title="WHEREtoRio", layout="wide")

# Configuração inicial
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

navbar = BaseScreen.render_navbar()
styles = BaseScreen.apply_custom_styles()
banner = BaseScreen.render_banner()

# Controle de navegação
if st.session_state["current_page"] == "Home":
    home_screen = HomeScreen()
    home_screen.render()
     
elif st.session_state["current_page"] == "Meus Roteiros":
    response_screen = ResponseScreen(trip)
    response_screen.render()

elif st.session_state["current_page"] == "Register":
    register_screen = RegisterScreen()
    register_screen.render()

elif st.session_state["current_page"] == "Login":
    login_screen = LoginScreen()
    login_screen.render()

footer = BaseScreen.render_footer()