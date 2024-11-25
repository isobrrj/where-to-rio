import streamlit as st
from base_screen import render_navbar, render_footer, apply_custom_styles, render_banner

def render_home():
    """
    Renderiza a página inicial.
    """

    # Conteúdo principal centralizado
    st.markdown(
        """
        <div style="text-align: center; margin: 40px auto; font-family: Arial, sans-serif;">
            <p style="font-size: 20px; line-height: 1.6; color: #555;">
                Descubra os melhores destinos turísticos no Rio de Janeiro! Explore praias paradisíacas, 
                pontos históricos e culturais, e os segredos mais encantadores da Cidade Maravilhosa. 
                Deixe-nos guiar você em uma viagem inesquecível!
            </p>
            <div style="margin-top: 30px;">
                <a href="#" style="
                    display: inline-block;
                    background-color: #90e0ef;
                    color: #023e8a;
                    text-decoration: none;
                    padding: 15px 25px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                    margin: 10px;
                    transition: background-color 0.3s ease, color 0.3s ease;">
                    Crie Seu Perfil e Descubra Sua Rota Ideal!
                </a>
                <a href="#" style="
                    display: inline-block;
                    background-color: #90e0ef;
                    color: #023e8a;
                    text-decoration: none;
                    padding: 15px 25px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                    margin: 10px;
                    transition: background-color 0.3s ease, color 0.3s ease;">
                    Buscar um passeio
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
