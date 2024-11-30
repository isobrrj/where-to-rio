import streamlit as st
from utils.auth.auth_users import AuthUser
from request_screen import RequestScreen
from trip_guide_builder import TripGuideBuilder
from utils.pages import Pages

authenticator = AuthUser()
login_status = authenticator.login()

pages = Pages()

if st.session_state["authentication_status"]:
    authenticator.logout()
    pages.page_flow()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    request_screen = RequestScreen()
    tourism_preference = request_screen.collect_tourism_preference()
    if tourism_preference:
        trip_guide_buider = TripGuideBuilder(tourism_preference=tourism_preference)
        question = trip_guide_buider.build_question_message_llm()
        # suggestion = trip_guide_buider.ask_chat_gpt(question)
        suggestion = """
            Dia 02/12/2024 (Domingo) - Manhã - Centro Cultural Banco do Brasil - CCBB Rio de Janeiro
            Localização: Rua Primeiro de Março, 66, Rio de Janeiro, Estado do Rio de Janeiro 20010-000 Brasil
            Descrição: Inaugurado em 12 de outubro de 1989, o Centro Cultural Banco do Brasil Rio de Janeiro transformou-se rapidamente em um dos centros culturais mais importantes do País. Na lista dos 100 museus mais visitados do mundo em 2016 da publicação inglesa The Art Newspaper, o Centro Cultural do Banco do Brasil no Rio de Janeiro ocupa a 26ª colocação com 2.216.880 visitantes.

            Dia 02/12/2024 (Domingo) - Tarde - Praia de Copacabana
            Localização: Copacabana, Brasil
            Descrição: A Praia de Copacabana é uma praia localizada no bairro de Copacabana, na Zona Sul da cidade do Rio de Janeiro, no Brasil. É considerada uma das praias mais famosas do mundo.

            Dia 03/12/2024 (Segunda-Feira) - Manhã - Praia de Ipanema
            Localização: Avenida Vieira Souto, Rio de Janeiro, Estado do Rio de Janeiro 22420-002 Brasil
            Descrição: Esta é uma praia bastante badalada no Rio, frequentada por artistas, jovens, turistas e moradores que aproveitam seu calçadão para a prática de exercícios. A praia do bairro nobre é um dos points da cidade quando o assunto é curtir o mar e tem uma parte destinada ao público LGBT+. As condições do mar dependem do período, mas muitas vezes o mar é tranquilo, com ondas fracas.

            Dia 03/12/2024 (Segunda-Feira) - Tarde - Centro Cultural Banco do Brasil - CCBB Rio de Janeiro
            Localização: Rua Primeiro de Março, 66, Rio de Janeiro, Estado do Rio de Janeiro 20010-000 Brasil
            Descrição: Inaugurado em 12 de outubro de 1989, o Centro Cultural Banco do Brasil Rio de Janeiro transformou-se rapidamente em um dos centros culturais mais importantes do País. Na lista dos 100 museus mais visitados do mundo em 2016 da publicação inglesa The Art Newspaper, o Centro Cultural do Banco do Brasil no Rio de Janeiro ocupa a 26ª colocação com 2.216.880 visitantes.

            Dia 03/12/2024 (Segunda-Feira) - Noite - Praia de Copacabana
            Localização: Copacabana, Brasil
            Descrição: A Praia de Copacabana é uma praia localizada no bairro de Copacabana, na Zona Sul da cidade do Rio de Janeiro, no Brasil. É considerada uma das praias mais famosas do mundo.
        """
        trip_guide_day = trip_guide_buider.build_trip_guide_day(suggestion)
        st.write(str(trip_guide_day))

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha inválido')

elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')
