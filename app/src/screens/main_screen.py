import streamlit as st
from home_screen import render_home
from base_screen import render_navbar, render_banner, render_footer, apply_custom_styles
from response_screen import render_response

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
render_footer()