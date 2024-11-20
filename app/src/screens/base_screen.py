import streamlit as st
import os

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
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 18px;
            width: 100%; /* Garante que ocupe toda a largura da tela */
        }
        .navbar-links {
            display: flex;
            gap: 30px;
        }
        .navbar-links a {
            color: white;
            text-decoration: none;
            font-weight: bold;
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
            position: fixed; /* Fixo na parte inferior da tela */
            bottom: 0; /* Alinha o footer na borda inferior */
            left: 0; /* Garante que comece na borda esquerda */
            width: 100vw; /* Usa 100% da largura da viewport */
            font-family: Arial, sans-serif;
            font-size: 14px;
            z-index: 1000; /* Certifica que o footer está acima de outros elementos */
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_navbar():
    """
    Renderiza a barra de navegação no topo da página.
    """
    st.markdown(
        """
        <div class="navbar">
            <!-- Links à esquerda -->
            <div class="navbar-links">
                <a href="#">Home</a>
                <a href="#">Meus Roteiros</a>
                <a href="#">Sobre</a>
            </div>
            <!-- Informações do usuário à direita -->
            <div class="user-info">
                <span>Olá, Usuário!</span>
                <button>Sair</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_banner():
    """
    Renderiza o banner com a imagem e o texto centralizado na frente.
    """
    # Caminho absoluto da imagem na pasta 'images'
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'banner.jpg'))

    # CSS para cortar a parte superior e inferior
    st.markdown(
        f"""
        <style>
        .banner-container {{
            position: relative;
            width: 100%;
            height: 80%; /* Altura ajustada do banner */
            overflow: hidden;
        }}
        .banner-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .banner-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 72px; /* Tamanho do texto */
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            z-index: 10;
        }}
        </style>
        <div class="banner-container">
            <img src="data:image/jpeg;base64,{get_base64_image(image_path)}" class="banner-image" alt="Banner">
            <div class="banner-text">WHEREtoRio</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_base64_image(image_path):
    """
    Converte a imagem para base64 para permitir a incorporação em HTML.
    """
    import base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


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
