from database.sessionmanager import SessionManager
from database.models import AttractionType
from tripguide.trip_guide_builder import TripGuideBuilder
from tripguide.attraction_manager import AttractionManager
from tripguide.itinerary_manager import ItineraryManager


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

        # Processar as sugestões
        trip_guide_day = trip_guide_builder.build_trip_guide_day(suggestion)

        # Processar as preferências e obter os IDs dos tipos de atrações
        preferences = self.process_preferences()

         # Mapear o orçamento para um número
        numeric_budget = self.map_budget_to_number()

        # Criar o itinerário no banco
        success = self.itinerary_manager.create_itinerary(
            user_id=self.user_id,
            start_date=self.tourism_preference.init_date,
            end_date=self.tourism_preference.end_date,
            budget=numeric_budget,  # Ajuste o orçamento conforme necessário
            preference=preferences # Ajuste as preferências conforme necessário
        )

        if success:
            return "Roteiro criado com sucesso!"
        else:
            return "Erro ao criar o roteiro."
