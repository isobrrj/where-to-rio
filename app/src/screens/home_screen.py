import streamlit as st
from page_manager import PageManager

class HomeScreen:
    """
    Classe responsável por renderizar a página inicial.
    """

    @staticmethod
    def render():
        """
        Renderiza o conteúdo principal da página inicial.
        """
        st.markdown(
            """
            <div style="text-align: center; margin: 40px auto; font-family: Arial, sans-serif;">
                <p style="font-size: 20px; line-height: 1.6; color: #555;">
                    Descubra os melhores destinos turísticos no Rio de Janeiro! Explore praias paradisíacas, 
                    pontos históricos e culturais, e os segredos mais encantadores da Cidade Maravilhosa. 
                    Deixe-nos guiar você em uma viagem inesquecível!
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Botões para navegação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Crie Seu Perfil e Descubra Sua Rota Ideal!"):
                # Verifica se o usuário está logado
                if st.session_state.get("logged_in", False):
                    PageManager.set_page("RequestScreen")
                else:
                    st.warning("Por favor, faça login para acessar esta funcionalidade.")
                    PageManager.set_page("Login")
        with col2:
            if st.button("Buscar um passeio"):
                PageManager.set_page("SearchTrips")
