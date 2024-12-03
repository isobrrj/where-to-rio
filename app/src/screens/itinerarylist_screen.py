from page_manager import PageManager
import streamlit as st
from tripguide.itinerary_manager import ItineraryManager

class ItineraryListScreen:
    """
    Classe responsável por renderizar a tela de lista de roteiros.
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.itinerary_manager = ItineraryManager()

    def render(self):
        """
        Renderiza a página com a lista de roteiros do usuário.
        """
        st.markdown(
            """
            <h1 style="text-align: center;font-family: Montserrat; font-size: 36px; color: #333;">
                Meus Roteiros
            </h1>
            """,
            unsafe_allow_html=True
        )

        itineraries = self.itinerary_manager.get_user_itineraries()

        if not itineraries:
            st.warning("Você ainda não criou nenhum roteiro.")
            return

        # CSS para centralizar os botões no meio da página
        st.markdown(
            """
            <style>
            .container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: auto;
            }
            .button-container {
                margin: 10px 0;
                width: 100%;
                max-width: 400px;
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Renderizando os botões dentro do contêiner centralizado
        st.markdown('<div class="container">', unsafe_allow_html=True)
        for idx, itinerary in enumerate(itineraries):  # Adicionando um índice para gerar chaves únicas
            itinerary_id = itinerary.itinerary_id
            start_date = itinerary.start_date.strftime("%d/%m/%Y")
            end_date = itinerary.end_date.strftime("%d/%m/%Y")
            button_label = f"Roteiro de {start_date} a {end_date}"

            st.markdown(f'<div class="button-container">', unsafe_allow_html=True)
            if st.button(button_label, key=f"button_{idx}"):
                # Verifica se o usuário está logado
                if st.session_state.get("logged_in", False):
                    PageManager.set_page("Roteiro", itinerary_id=itinerary_id)
                else:
                    st.warning("Por favor, faça login para acessar esta funcionalidade.")
                    PageManager.set_page("Login")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)