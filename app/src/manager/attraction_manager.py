from database.sessionmanager import SessionManager
from database.models import Attraction
import pandas as pd


class AttractionManager:
    """
    Classe para gerenciar as operações relacionadas à tabela Attraction.
    """

    def __init__(self):
        self.session = SessionManager()

    def get_attraction_by_name(self, name):
        """
        Busca uma atração pelo nome.
        :param name: Nome da atração.
        :return: Objeto Attraction se encontrado, ou None.
        """
        try:
            return self.session.query(Attraction).filter(Attraction.name == name).first()
        except Exception as e:
            print(f"Erro ao buscar a atração {name}: {e}")
            return None

    def insert_attraction(self, name, operating_hours, description, attraction_type, location, photo=None):
        """
        Insere uma nova atração na tabela Attraction.

        :param name: Nome da atração.
        :param operating_hours: Horário de funcionamento.
        :param description: Descrição da atração.
        :param attraction_type: Tipo da atração (ID da chave estrangeira).
        :param time_of_day: Período do dia associado à atração.
        :param photo: Caminho ou URL da foto da atração (opcional).
        """
        try:
            # Cria uma instância de Attraction
            attraction = Attraction(
                name=name,
                operating_hours=operating_hours,
                description=description,
                attraction_type=attraction_type,
                photo=photo,
                location=location
            )

            # Adiciona a instância ao banco de dados
            self.session.add(attraction)
            self.session.commit()
            print(f"Atração {name} inserida com sucesso!")
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao inserir a atração: {e}")
        finally:
            self.session.close()

    def __del__(self):
        """
        Fecha a sessão quando a instância de AttractionManager é destruída.
        """
        self.session.close()


if __name__ == "__main__":
    attr_df = pd.read_csv("chat_gpt/attractions.csv")
    print(attr_df.head())
