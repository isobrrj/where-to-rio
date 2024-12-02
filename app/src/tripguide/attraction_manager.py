from database.sessionmanager import SessionManager
from database.models import Attraction

class AttractionManager:
    """
    Classe para gerenciar as operações relacionadas à tabela Attraction.
    """

    def __init__(self):
        self.session = SessionManager()

    def insert_attraction(self, name, operating_hours, description, attraction_type, photo=None):
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
