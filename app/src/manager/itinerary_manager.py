from datetime import timedelta
from database.sessionmanager import SessionManager
from database.models import Attraction, Includes, Itinerary, Owns
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import streamlit as st

class ItineraryManager:
    """
    Classe responsável por gerenciar operações relacionadas às tabelas Itinerary e Owns.
    """

    def __init__(self):
        self.session_manager = SessionManager()

    def create_itinerary(self, user_id, start_date, end_date, user_location, budget=None, preference=None):
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
                    budget=budget,
                    user_location=user_location
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
            
    def get_itinerary_data(self, itinerary_id):
        """
        Obtém os dados completos de um itinerário pelo ID, incluindo as atrações, organizadas por data.
        :param itinerary_id: ID do itinerário a ser buscado.
        """
        with self.session_manager as session:
            try:
                # Busca o itinerário pelo ID
                itinerary = (
                    session.query(Itinerary)
                    .filter(Itinerary.itinerary_id == itinerary_id)
                    .first()
                )

                if not itinerary:
                    return None

                # Organizar os dados do itinerário
                itinerary_data = {
                    "itinerary_id": itinerary.itinerary_id,
                    "start_date": itinerary.start_date,
                    "end_date": itinerary.end_date,
                    "budget": itinerary.budget,
                    "user_location": itinerary.user_location,
                    "days": []  # Lista de dias com atividades
                }

                # Gera os dias do itinerário
                current_date = itinerary.start_date
                while current_date <= itinerary.end_date:  # Inclui a data final no intervalo
                    itinerary_data["days"].append({
                        "date": current_date,
                        "day_of_week": current_date.strftime("%A"),
                        "activities": {
                            "morning": [],
                            "afternoon": [],
                            "evening": []
                        }
                    })
                    current_date += timedelta(days=1)

                # Busca as atividades associadas ao itinerário
                includes = (
                    session.query(Includes)
                    .filter(Includes.itinerary_id == itinerary.itinerary_id)
                    .all()
                )

                # Organiza as atividades nos dias correspondentes
                for include in includes:
                    time_of_day = include.time_of_day.lower()
                    attraction = (
                        session.query(Attraction)
                        .filter(Attraction.attraction_id == include.attraction_id)
                        .first()
                    )

                    if attraction:
                        # Adiciona a atividade ao dia correto baseado na data da tabela Includes
                        for day in itinerary_data["days"]:
                            if day["date"] == include.date:  # Usa a data diretamente da tabela Includes
                                day["activities"][time_of_day].append({
                                    "name": attraction.name,
                                    "description": attraction.description,
                                    "operating_hours": attraction.operating_hours,
                                    "location": attraction.location
                                })

                return itinerary_data

            except Exception as e:
                print(f"Erro ao buscar os dados do itinerário: {e}")
                return None
        
    def add_to_includes(self, itinerary_id, attraction_id, time_of_day, date):
        """
        Adiciona uma entrada à tabela Includes.
        :param itinerary_id: ID do itinerário.
        :param attraction_id: ID da atração.
        :param time_of_day: Período do dia (ex: "Manhã", "Tarde", "Noite").
        :param date: Data da atividade.
        """
        try:
            new_include = Includes(
                itinerary_id=itinerary_id,
                attraction_id=attraction_id,
                time_of_day=time_of_day,
                date=date
            )
            self.session_manager.add(new_include)
            self.session_manager.commit()
            print(f"Adicionado à tabela Includes: {itinerary_id} - {attraction_id} - {date}")
        except Exception as e:
            self.session_manager.rollback()
            print(f"Erro ao adicionar à tabela Includes: {e}")

    def get_user_itineraries(self):
        """
        Retorna todos os itinerários associados a um usuário específico.
        :param user_id: ID do usuário.
        :return: Lista de itinerários.
        """
        user_id = st.session_state.get("user_id")

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
