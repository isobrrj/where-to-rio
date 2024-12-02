import streamlit as st
from screens.request_screen import RequestScreen
from tripguide.trip_guide_builder import TripGuideBuilder
from utils.pages import Pages
from screens.login_screen import LoginScreen

def main():
    # Configuração inicial do estado
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False  # Define o estado inicial de login
        st.session_state["user_id"] = None     # ID do usuário logado

    # Autenticação
    if not st.session_state["logged_in"]:
        login_screen = LoginScreen()
        login_screen.render()
    else:
        # Renderiza o restante da aplicação após o login
        st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"logged_in": False, "user_id": None}))
        st.write(f"Bem-vindo, {st.session_state['user_name']}!")

        # Fluxo da aplicação
        pages = Pages()
        pages.page_flow()

        request_screen = RequestScreen()
        tourism_preference = request_screen.render()
        if tourism_preference:
            trip_guide_builder = TripGuideBuilder(tourism_preference=tourism_preference)
            question = trip_guide_builder.build_question_message_llm()
            
            # suggestion = trip_guide_buider.ask_chat_gpt(question)

            suggestion = """
            Dia 02/12/2024 (Domingo) - Manhã - Centro Cultural Banco do Brasil - CCBB Rio de Janeiro
            Localização: Rua Primeiro de Março, 66, Rio de Janeiro, Estado do Rio de Janeiro 20010-000 Brasil
            Descrição: Inaugurado em 12 de outubro de 1989...
            """
            
            trip_guide_day = trip_guide_builder.build_trip_guide_day(suggestion)
            st.write(str(trip_guide_day))

if __name__ == "__main__":
    main()
