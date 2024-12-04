from database.sessionmanager import SessionManager
from database.models import AttractionType
from tripguide.trip_guide_builder import TripGuideBuilder
from tripguide.attraction_manager import AttractionManager
from tripguide.itinerary_manager import ItineraryManager
import streamlit as st

class TripPlanner:
    """
    Classe responsável por gerenciar a criação de roteiros e inserções no banco.
    """

    def __init__(self, tourism_preference, user_id):
        """
        Inicializa a classe com preferências de turismo e ID do usuário.
        :param tourism_preference: Objeto contendo as preferências do usuário.
        :param user_id: ID do usuário logado.
        """
        self.tourism_preference = tourism_preference
        self.user_id = user_id
        self.attraction_manager = AttractionManager()
        self.itinerary_manager = ItineraryManager()

    def process_preferences(self):
        """
        Processa as preferências do usuário e retorna os IDs dos tipos de atrações e restaurantes.
        :return: Uma string contendo os IDs dos tipos de atrações e restaurantes separados por vírgulas.
        """
        session = SessionManager()  # Obtém a sessão do banco de dados
        try:
            # Lista para armazenar os IDs de attraction_type e restaurant_type
            preferences_ids = []

            # Processar attr_preferences comparando com attraction_type
            for attr_pref, is_selected in self.tourism_preference.attr_preferences.items():
                if is_selected:
                    # Consultar o banco de dados para encontrar o attraction_type_id correspondente
                    attraction_type = (
                        session.query(AttractionType)
                        .filter(AttractionType.attraction_type.ilike(attr_pref))
                        .first()
                    )
                    if attraction_type:
                        preferences_ids.append(str(attraction_type.attraction_type_id))

            # Processar lunch_preferences comparando com restaurant_type
            for lunch_pref, is_selected in self.tourism_preference.lunch_preferences.items():
                if is_selected:
                    # Consultar o banco de dados para encontrar o restaurant_type_id correspondente
                    restaurant_type = (
                        session.query(AttractionType)
                        .filter(AttractionType.restaurant_type.ilike(lunch_pref))
                        .first()
                    )
                    if restaurant_type:
                        preferences_ids.append(str(restaurant_type.attraction_type_id))

            # Retorna os IDs como uma string separada por vírgulas
            return ",".join(preferences_ids)
        except Exception as e:
            print(f"Erro ao processar preferências: {e}")
            return ""
        finally:
            session.close()
    
    def map_budget_to_number(self):
        """
        Mapeia o valor do orçamento para um número correspondente.
        :return: Um número de 1 a 4 correspondente ao orçamento.
        """
        budget_mapping = {
            "$": 1,
            "$$": 2,
            "$$$": 3,
            "$$$$+": 4
        }
        return budget_mapping.get(self.tourism_preference.budget, 1)  # Padrão é 1 (menor orçamento)

    def process_trip(self):
        """
        Processa as preferências do usuário para criar um roteiro.
        """
        trip_guide_builder = TripGuideBuilder(tourism_preference=self.tourism_preference)
        question = trip_guide_builder.build_question_message_llm()
        st.write(question)
        suggestion = trip_guide_builder.ask_chat_gpt_about_attractions(question)
        st.write(suggestion)
        # Obter sugestões do modelo (aqui está mockado)
        #     suggestion = """
        #     Dia 03/12/2024 (Terça-Feira) - Manhã - Maracanã Descrição: Estádio Jornalista Mário Filho, mais conhecido como Maracanã, ou carinhosamente como Maraca, é um estádio de futebol localizado no bairro de mesmo nome, na Zona Norte da cidade brasileira do Rio de Janeiro. Localização: R. Prof. Eurico Rabelo - Maracanã, Rio de Janeiro - RJ, 20271-150 Categoria de Atração: Principais Pontos Turísticos
        #     Dia 03/12/2024 (Terça-Feira) - Tarde - Praia de Copacabana Descrição: A Praia de Copacabana é uma praia localizada no bairro de Copacabana, na Zona Sul da cidade do Rio de Janeiro, no Brasil. É considerada uma das praias mais famosas do mundo. Localização: Copacabana; Brasil Categoria de Atração: Praias
        #     Dia 03/12/2024 (Terça-Feira) - Noite - Praia de Ipanema Descrição: Esta é uma praia bastante badalada no Rio, frequentada por artistas, jovens, turistas e moradores que aproveitam seu calçadão para a prática de exercícios. A praia do bairro nobre é um dos points da cidade quando o assunto é curtir o mar e tem uma parte destinada ao público LGBT+. As condições do mar dependem do período, mas muitas vezes o mar é tranquilo, com ondas fracas. Localização: Avenida Vieira Souto, Rio de Janeiro, Estado do Rio de Janeiro 22420-002 Brasil Categoria de Atração: Praias
        #     Dia 04/12/2024 (Quarta-Feira) - Manhã - Parque Lage Descrição: O Parque Lage é um parque público no bairro Jardim Botânico, na Zona Sul do Rio de Janeiro. Possui trilhas, jardins, um belo palacete e uma vista incrível para o Cristo Redentor. Localização: R. Jardim Botânico, 414 - Jardim Botânico, Rio de Janeiro - RJ, 22461-000 Categoria de Atração: Parques e Trilhas
        #     Dia 04/12/2024 (Quarta-Feira) - Tarde - Museu Histórico Nacional Descrição: O Museu Histórico Nacional é um museu localizado na Praça Marechal Âncora, no centro histórico do Rio de Janeiro. Possui um acervo que conta a história do Brasil desde a época do descobrimento. Localização: Praça Marechal Âncora, S/N - Centro, Rio de Janeiro - RJ, 20021-200 Categoria de Atração: Patrimônio Histórico e Cultural
        #     Dia 04/12/2024 (Quarta-Feira) - Noite - Pão de Açúcar Descrição: O Pão de Açúcar é um dos principais pontos turísticos do Rio de Janeiro. É um complexo de morros localizado na entrada da Baía de Guanabara, no bairro da Urca, com uma vista panorâmica incrível da cidade. Localização: Av. Pasteur, 520 - Urca, Rio de Janeiro - RJ, 22290-255 Categoria de Atração: Principais Pontos Turísticos
        #     Dia 05/12/2024 (Quinta-Feira) - Manhã - Jardim Botânico Descrição: O Jardim Botânico do Rio de Janeiro é um dos mais importantes do Brasil, com uma grande diversidade de plantas e árvores. Possui uma estufa de plantas raras, lagos e trilhas para caminhada. Localização: R. Jardim Botânico, 1008 - Jardim Botânico, Rio de Janeiro - RJ, 22460-030 Categoria de Atração: Parques e Trilhas
        #     Dia 05/12/2024 (Quinta-Feira) - Tarde - Museu do Amanhã Descrição: O Museu do Amanhã é um museu de ciências localizado na Praça Mauá, na região portuária do Rio de Janeiro. Possui exposições interativas sobre sustentabilidade, meio ambiente e o futuro da humanidade. Localização: Praça Mauá, 1 - Centro, Rio de Janeiro - RJ, 20081-240 Categoria de Atração: Patrimônio Histórico e Cultural
        #     Dia 05/12/2024 (Quinta-Feira) - Noite - Lapa Descrição: A Lapa é um bairro boêmio do Rio de Janeiro, conhecido pelos seus arcos, bares, casas de show e vida noturna agitada. É um local tradicional para quem busca diversão e música ao vivo. Localização: Lapa, Rio de Janeiro - RJ Categoria de Atração: Principais Pontos Turísticos
        #     Espero que aproveite sua viagem e as sugestões de roteiro!
        # """

        # Processar as sugestões
        trip_guide_day = trip_guide_builder.build_trip_guide_day(suggestion)
        st.write(trip_guide_day)
        # Processar as preferências e obter os IDs dos tipos de atrações
        preferences = self.process_preferences()

        # Mapear o orçamento para um número
        numeric_budget = self.map_budget_to_number()

        # Criar o itinerário no banco
        itinerary_id = self.itinerary_manager.create_itinerary(
            user_id=self.user_id,
            start_date=self.tourism_preference.init_date,
            end_date=self.tourism_preference.end_date,
            budget=numeric_budget,
            preference=preferences
        )

        if itinerary_id:
            # Adicionar as atrações sugeridas à tabela Includes
            for day in trip_guide_day.days:
                day_date = day.date  # A data do dia no TripGuideDay
                for period in ["morning", "afternoon", "evening"]:
                    for activity in getattr(day, period):
                        self.itinerary_manager.add_to_includes(
                            itinerary_id=itinerary_id,
                            attraction_id=self._get_or_create_attraction(activity),
                            time_of_day=period.capitalize(),
                            date=day_date
                        )

            return "Roteiro criado com sucesso!"
        else:
            return "Erro ao criar o roteiro."

    def _get_or_create_attraction(self, activity):
        """
        Verifica se a atração já existe no banco ou cria uma nova.
        :param activity: Dicionário contendo os detalhes da atividade.
        :return: ID da atração.
        """
        name = activity["name"]
        description = activity.get("description", "Descrição não fornecida")
        operating_hours = activity.get("operating_hours", "Horário não especificado")

        # Verifica se a atração já existe no banco
        existing_attraction = self.attraction_manager.get_attraction_by_name(name)
        if existing_attraction:
            return existing_attraction.attraction_id

        # Se não existir, cria uma nova atração
        self.attraction_manager.insert_attraction(
            name=name,
            operating_hours=operating_hours,
            description=description,
            attraction_type=1,
            photo=None
        )

        new_attraction = self.attraction_manager.get_attraction_by_name(name)
        if new_attraction:
            return new_attraction.attraction_id
        else:
            raise ValueError(f"Erro ao criar ou recuperar a atração: {name}")
