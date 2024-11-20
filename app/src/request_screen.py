from src.utils.screen_template import ScreenTemplate
import streamlit as st


class RequestScreen(ScreenTemplate):
    def show_window(self):
        st.title("Solicitação de roteiro")
        st.write("Preencha o formulário com informações sobre sua viagem e preferências para geração de uma sugestão de roteiro")

        init_date =  st.date_input("Primeiro dia do Roteiro")
        end_date = st.date_input("Último dia do Roteiro")
        neigh = st.text_input("Bairro em que estará hospedado")

        preferences = {}
        preferences["Patrimônio Histórico e Cultural"] = st.checkbox("Patrimônio Histórico e Cultural")
        preferences["Parques e Trilhas"] = st.checkbox("Parques e Trilhas")
        preferences["Principais Pontos Turísticos"] = st.checkbox("Principais Pontos Turísticos")
        preferences["Praias"] = st.checkbox("Praias")
        preferences["Arquitetura e Infraestrutura Urbana"] = st.checkbox("Arquitetura e Infraestrutura Urbana")
        preferences["Entretenimento e Lazer"] = st.checkbox("Entretenimento e Lazer")
        preferences["Compras"] = st.checkbox("Compras")
        preferences["Vida Noturna"] = st.checkbox("Vida Noturna")

        return init_date, end_date,  neigh, preferences