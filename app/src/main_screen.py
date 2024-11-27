import streamlit as st
from screens.home_screen import render_home
from screens.base_screen import render_navbar, render_banner, render_footer, apply_custom_styles
from screens.response_screen import render_response
from screens.register_screen import render_register

# Configuração inicial da página
st.set_page_config(page_title="WHEREtoRio", layout="wide")

# Configuração inicial
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

apply_custom_styles()
render_navbar()
render_banner()

# Controle de navegação
if st.session_state["current_page"] == "Home":
    render_home()
     
elif st.session_state["current_page"] == "Meus Roteiros":
    render_response()

elif st.session_state["current_page"] == "Register":
    render_register()

render_footer()