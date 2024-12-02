from database.sessionmanager import SessionManager
from database.models import Includes, Itinerary, Owns
from sqlalchemy.exc import SQLAlchemyError


class ItineraryManager:
    """
    Classe responsável por gerenciar operações relacionadas às tabelas Itinerary e Owns.
    """

    def __init__(self):
        self.session_manager = SessionManager()

    def create_itinerary(self, user_id, start_date, end_date, budget=None, preference=None):
        """
        Cria um novo Itinerary e associa ao usuário logado via tabela Owns.
        :param user_id: ID do usuário logado.
        :param start_date: Data de início do itinerário.
        :param end_date: Data de término do itinerário.
        :param budget: Orçamento associado ao itinerário.
        :param preference: Preferência opcional para a tabela Owns.
        :return: ID do itinerário criado se bem-sucedido, None em caso de erro.
        """
        with self.session_manager as session:
            try:
                # Verifica se as datas são válidas
                if start_date >= end_date:
                    raise ValueError("A data de início deve ser anterior à data de término.")

                # Criar o Itinerary
                new_itinerary = Itinerary(
                    start_date=start_date,
                    end_date=end_date,
                    budget=budget
                )
                session.add(new_itinerary)
                session.flush()  # Garante que o ID do itinerário seja gerado

                # Criar o vínculo na tabela Owns
                new_owns = Owns(
                    user_id=user_id,
                    itinerary_id=new_itinerary.itinerary_id,
                    preference=preference
                )
                session.add(new_owns)
                session.commit()

                print(f"Itinerário {new_itinerary.itinerary_id} criado e associado ao usuário {user_id}.")
                return new_itinerary.itinerary_id
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Erro ao criar Itinerary ou associar ao usuário: {e}")
                return None
        
    def add_to_includes(self, itinerary_id, attraction_id, time_of_day):
        """
        Adiciona uma entrada à tabela Includes.
        :param itinerary_id: ID do itinerário.
        :param attraction_id: ID da atração.
        :param time_of_day: Período do dia (ex: "Manhã", "Tarde", "Noite").
        """
        try:
            new_include = Includes(
                itinerary_id=itinerary_id,
                attraction_id=attraction_id,
                time_of_day=time_of_day
            )
            self.session_manager.add(new_include)
            self.session_manager.commit()
            print(f"Adicionado à tabela Includes: {itinerary_id} - {attraction_id}")
        except Exception as e:
            self.session_manager.rollback()
            print(f"Erro ao adicionar à tabela Includes: {e}")

    def get_user_itineraries(self, user_id):
        """
        Retorna todos os itinerários associados a um usuário específico.
        :param user_id: ID do usuário.
        :return: Lista de itinerários.
        """
        with self.session_manager as session:
            try:
                itineraries = (
                    session.query(Itinerary)
                    .join(Owns, Owns.itinerary_id == Itinerary.itinerary_id)
                    .filter(Owns.user_id == user_id)
                    .all()
                )
                return itineraries
            except SQLAlchemyError as e:
                print(f"Erro ao buscar itinerários do usuário {user_id}: {e}")
                return []

    def delete_itinerary(self, itinerary_id):
        """
        Remove um itinerário e todas as associações relacionadas.
        :param itinerary_id: ID do itinerário a ser removido.
        :return: True se bem-sucedido, False em caso de erro.
        """
        with self.session_manager as session:
            try:
                # Remover associações da tabela Owns
                session.query(Owns).filter(Owns.itinerary_id == itinerary_id).delete()

                # Remover o itinerário
                session.query(Itinerary).filter(Itinerary.itinerary_id == itinerary_id).delete()

                session.commit()
                print(f"Itinerário {itinerary_id} e suas associações foram removidos com sucesso.")
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Erro ao remover o itinerário {itinerary_id}: {e}")
                return False