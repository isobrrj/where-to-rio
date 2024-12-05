
import streamlit as st
from tripguide.trip_planner import TripPlanner
from manager.page_manager import PageManager
from screens.base_screen import BaseScreen
from streamlit_cookies_manager import EncryptedCookieManager

# Configuração inicial da página
st.set_page_config(page_title="WHEREtoRio", layout="wide")

# Inicializar o gerenciador de cookies
cookie_manager = EncryptedCookieManager(prefix="wheretoriorio", password="chave_secreta")

if not cookie_manager.ready():
    st.stop()  # Aguarda a inicialização do gerenciador de cookies

# Restaurar o estado de login a partir dos cookies
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = cookie_manager.get("logged_in", "false") == "true"
    st.session_state["user_id"] = int(cookie_manager.get("user_id", "0")) if cookie_manager.get("user_id") else None
    st.session_state["user_name"] = cookie_manager.get("user_name", "Visitante")

# Renderiza elementos comuns
navbar = BaseScreen.render_navbar(cookie_manager)
styles = BaseScreen.apply_custom_styles()
banner = BaseScreen.render_banner()

page_manager = PageManager(cookie_manager)  # Inicializa o gerenciador de páginas

# Renderiza a página atual e captura o resultado, se houver
result = page_manager.render_current_page()


# Processa o resultado, se for gerado pela página RequestScreen
if result:
    user_id = st.session_state["user_id"]

    # Cria uma instância do TripPlanner
    trip_planner = TripPlanner(tourism_preference=result, user_id=user_id)

    # Processa o roteiro
    message = trip_planner.process_trip()
    st.success(message)



footer = BaseScreen.render_footer()
