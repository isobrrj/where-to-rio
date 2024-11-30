import streamlit as st
import os
import base64
from screens.login_screen import AuthManager

class BaseScreen:
    """
    Classe responsável por gerenciar elementos básicos da interface, como navbar, banner e footer.
    """

    @staticmethod
    def apply_custom_styles():
        """
        Aplica estilos customizados para a página.
        """
        st.markdown(
            """
            <style>
            .navbar {
                background-color: #2B4E72;
                padding: 10px;
                position: fixed;
                left: 0;
                width: 100vw;
                font-family: Arial, sans-serif;
                font-size: 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: white;
                z-index: 1000;
            }
            .navbar-links {
                display: flex;
                gap: 30px;
            }
            .navbar-links a {
                color: white;
                text-decoration: none;
                font-weight: bold;
                cursor: pointer;
            }
            .navbar-links a:hover {
                text-decoration: underline;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .user-info button {
                background-color: #90e0ef;
                border: none;
                color: #023e8a;
                padding: 5px 15px;
                border-radius: 5px;
                cursor: pointer;
            }
            .user-info button:hover {
                background-color: #0077b6;
                color: white;
            }
            .footer {
                background-color: #2B4E72;
                color: white;
                text-align: center;
                padding: 10px 0;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100vw;
                font-family: Arial, sans-serif;
                font-size: 14px;
                z-index: 1000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def render_navbar(cookie_manager):
        """
        Renderiza a barra de navegação no topo da página com suporte a logout.
        """
        # Usando colunas para alinhar os botões horizontalmente
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 3])
        
        with col1:
            if st.button("Home"):
                BaseScreen.navigate_to("Home")
        with col2:
            if st.session_state.get("logged_in", True):
                if st.button("Meus Roteiros"):
                    BaseScreen.navigate_to("Meus Roteiros")
            else:
                if st.button("Registrar"):
                    BaseScreen.navigate_to("Register")
        with col3:
            if not st.session_state.get("logged_in", False):
                if st.button("Login"):
                    BaseScreen.navigate_to("Login")
            else:
                if st.button("Sair"):
                    AuthManager.logout(cookie_manager)  # Chama o método de logout
        
        # Exibição do nome do usuário ou mensagem padrão
        with col5:
            if st.session_state.get("logged_in", False):
                st.markdown(f"<div class='user-info'>Olá, {st.session_state['user_name']}!</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='user-info'>Olá, Visitante!</div>", unsafe_allow_html=True)


    @staticmethod
    def render_banner():
        """
        Renderiza o banner com a imagem e o texto centralizado.
        """
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'banner.jpg'))
        st.markdown(
            f"""
            <style>
            .banner-container {{
                position: relative;
                width: 100%;
                overflow: hidden;
            }}
            .banner-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 72px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
                z-index: 10;
            }}
            </style>
            <div class="banner-container">
                <img src="data:image/jpeg;base64,{BaseScreen.get_base64_image(image_path)}" alt="Banner" style="width: 100%;">
                <div class="banner-text">WHEREtoRio</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def get_base64_image(image_path):
        """
        Converte a imagem para base64 para permitir a incorporação em HTML.
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    @staticmethod
    def render_footer():
        """
        Renderiza o rodapé fixo na parte inferior da página.
        """
        st.markdown(
            """
            <div class="footer">
                © 2024 WHEREtoRio - Todos os direitos reservados
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def navigate_to(page_name):
        """
        Função para navegar entre páginas.
        """
        st.session_state["current_page"] = page_name
