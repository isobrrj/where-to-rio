from utils.screen_template import ScreenTemplate
import streamlit as st
from tourism_preference import TourismPreference


class RequestScreen(ScreenTemplate):
    def __init__(self) -> None:
        self.tourism_preference = TourismPreference(init_date=None,
                                                    end_date=None,
                                                    neigh=None,
                                                    preferences={})
    
    def __get_neighs(self):
        return [
            "Bairro Imperial de São Cristóvão", "Benfica", "Caju", "Catumbi", "Centro",
            "Cidade Nova", "Estácio", "Gamboa", "Glória", "Lapa", "Mangueira",
            "Paquetá", "Rio Comprido", "Santa Teresa", "Santo Cristo", "Saúde",
            "Vasco da Gama", "Abolição", "Acari", "Água Santa", "Aldeia Campista", "Alto da Boa Vista",
            "Anchieta", "Andaraí", "Bancários", "Barros Filho", "Bento Ribeiro",
            "Bonsucesso", "Brás de Pina", "Cachambi", "Cacuia", "Campinho",
            "Cascadura", "Cavalcanti", "Cidade Universitária", "Cocotá", "Coelho Neto",
            "Colégio", "Complexo do Alemão", "Cordovil", "Costa Barros", "Del Castilho",
            "Encantado", "Engenheiro Leal", "Engenho da Rainha", "Engenho de Dentro",
            "Engenho Novo", "Freguesia", "Galeão", "Grajaú", "Guadalupe",
            "Higienópolis", "Honório Gurgel", "Inhaúma", "Irajá", "Jacaré",
            "Jacarezinho", "Jardim América", "Jardim Carioca", "Jardim Guanabara",
            "Lins de Vasconcelos", "Madureira", "Manguinhos", "Maracanã", "Maré",
            "Marechal Hermes", "Maria da Graça", "Méier", "Moneró", "Olaria",
            "Oswaldo Cruz", "Parada de Lucas", "Parque Anchieta", "Parque Colúmbia",
            "Pavuna", "Penha", "Penha Circular", "Piedade", "Pilares", "Pitangueiras",
            "Portuguesa", "Praça da Bandeira", "Praia da Bandeira", "Quintino Bocaiúva",
            "Ramos", "Riachuelo", "Ribeira", "Ricardo de Albuquerque", "Rocha",
            "Rocha Miranda", "Sampaio", "São Francisco Xavier", "Tauá", "Tijuca",
            "Todos os Santos", "Tomás Coelho", "Turiaçu", "Vaz Lobo", "Vicente de Carvalho",
            "Vigário Geral", "Vila da Penha", "Vila Isabel", "Vila Kosmos", "Vista Alegre",
            "Zumbi", "Botafogo", "Catete", "Copacabana", "Cosme Velho", "Flamengo", "Gávea",
            "Humaitá", "Ipanema", "Jardim Botânico", "Lagoa", "Laranjeiras", "Leblon",
            "Leme", "Rocinha", "São Conrado", "Urca", "Vidigal", "Anil", "Bangu", "Barra da Tijuca", "Campo dos Afonsos", "Campo Grande",
            "Camorim", "Cidade de Deus", "Curicica", "Deodoro", "Freguesia (Jacarepaguá)",
            "Gardênia Azul", "Gericinó", "Grumari", "Guaratiba", "Inhoaíba", "Itanhangá",
            "Jacarepaguá", "Jardim Sulacap", "Joá", "Magalhães Bastos", "Paciência",
            "Padre Miguel", "Pedra de Guaratiba", "Pechincha", "Praça Seca", "Realengo",
            "Recreio dos Bandeirantes", "Santa Cruz", "Santíssimo", "Senador Camará",
            "Senador Vasconcelos", "Sepetiba", "Tanque", "Taquara", "Vargem Grande",
            "Vargem Pequena", "Vila Kennedy", "Vila Militar", "Vila Valqueire"
        ]

    def collect_tourism_preference(self):
        st.title("Solicitação de roteiro")
        st.write("Preencha o formulário com informações sobre sua viagem e preferências para geração de uma sugestão de roteiro")

        self.tourism_preference.init_date = st.date_input("Primeiro Dia do Roteiro", format="DD/MM/YYYY")
        self.tourism_preference.end_date = st.date_input("Último Dia do Roteiro", format="DD/MM/YYYY")
        self.tourism_preference.neigh = st.selectbox("Qual Bairro você estará hospedado?", self.__get_neighs())

        self.tourism_preference.preferences["Patrimônio Histórico e Cultural"] = st.checkbox("Patrimônio Histórico e Cultural")
        self.tourism_preference.preferences["Parques e Trilhas"] = st.checkbox("Parques e Trilhas")
        self.tourism_preference.preferences["Principais Pontos Turísticos"] = st.checkbox("Principais Pontos Turísticos")
        self.tourism_preference.preferences["Praias"] = st.checkbox("Praias")
        self.tourism_preference.preferences["Arquitetura e Infraestrutura Urbana"] = st.checkbox("Arquitetura e Infraestrutura Urbana")
        self.tourism_preference.preferences["Entretenimento e Lazer"] = st.checkbox("Entretenimento e Lazer")
        self.tourism_preference.preferences["Compras"] = st.checkbox("Compras")
        self.tourism_preference.preferences["Vida Noturna"] = st.checkbox("Vida Noturna")

        process_roteiro = st.button("Processar Roteiro")
        if process_roteiro:
            return self.tourism_preference
