import streamlit as st
from screens.home_screen import HomeScreen
from screens.base_screen import BaseScreen
from screens.response_screen import ResponseScreen
from screens.register_screen import RegisterScreen
from screens.login_screen import LoginScreen
from tripguide.test_trip_guide import trip
from streamlit_cookies_manager import EncryptedCookieManager

# Configuração inicial da página
st.set_page_config(page_title="WHEREtoRio", layout="wide")

# Inicializar o gerenciador de cookies
cookie_manager = EncryptedCookieManager(prefix="wheretoriorio", password="sua_chave_secreta")

if not cookie_manager.ready():
    st.stop()  # Aguarda a inicialização do gerenciador de cookies

# Restaurar o estado de login a partir dos cookies
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = cookie_manager.get("logged_in", "false") == "true"
    st.session_state["user_id"] = int(cookie_manager.get("user_id", "0")) if cookie_manager.get("user_id") else None
    st.session_state["user_name"] = cookie_manager.get("user_name", "Visitante")

# Configuração inicial do estado
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

# Renderiza elementos comuns
navbar = BaseScreen.render_navbar(cookie_manager)
styles = BaseScreen.apply_custom_styles()
banner = BaseScreen.render_banner()

# Renderizar a página correspondente
if st.session_state["current_page"] == "Home":
    home_screen = HomeScreen()
    home_screen.render()
elif st.session_state["current_page"] == "Meus Roteiros" and st.session_state["logged_in"]:
    response_screen = ResponseScreen(trip)
    response_screen.render()
elif st.session_state["current_page"] == "Register" and not st.session_state["logged_in"]:
    register_screen = RegisterScreen()
    register_screen.render()
elif st.session_state["current_page"] == "Login" and not st.session_state["logged_in"]:
    login_screen = LoginScreen(cookie_manager)
    login_screen.render()

footer = BaseScreen.render_footer()
