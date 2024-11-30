import streamlit as st
from trip_guide_builder import TripGuideBuilder
from page_manager import PageManager
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
    trip_guide_builder = TripGuideBuilder(tourism_preference=result)
    question = trip_guide_builder.build_question_message_llm()

    suggestion = """
    Dia 02/12/2024 (Domingo) - Manhã - Centro Cultural Banco do Brasil - CCBB Rio de Janeiro
    Localização: Rua Primeiro de Março, 66, Rio de Janeiro, Estado do Rio de Janeiro 20010-000 Brasil
    Descrição: Inaugurado em 12 de outubro de 1989...
    """
    
    trip_guide_day = trip_guide_builder.build_trip_guide_day(suggestion)
    st.write(str(trip_guide_day))


footer = BaseScreen.render_footer()
