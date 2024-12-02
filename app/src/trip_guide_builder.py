from openai_tourism_agent.rio_attraction_ml import RioAttractionML
from trip_guide import Day, TripGuideDay
import re
from datetime import datetime
from database.config import DATABASE_URL


class TripGuideBuilder:
    def __init__(self, tourism_preference) -> None:
        self.tourism_preference = tourism_preference

    def build_question_message_llm(self):
        str_question = f"Quais pontos turisticos posso visitar, durante minha viagem, entre o dia {self.tourism_preference.init_date} e {self.tourism_preference.end_date} no Rio de Janeiro? Estarei hospedado no bairro {self.tourism_preference.neigh} e  e tenho preferência por conhecer: "
        for k in self.tourism_preference.attr_preferences:
            if self.tourism_preference.attr_preferences[k]:
                str_question += f" {k},"
        str_question = str_question[:-1] + "."
        return str_question

    def ask_chat_gpt_about_attractions(self, question):
        query = """
    	    SELECT
                a.name AS "Nome da Atração",
                a.operating_hours AS "Dias e Turnos de Funcionamento",	
                a.description AS "Descrição",
                a.location AS "Localização",
                at2." attraction_type" AS "Categoria de Atração"
            FROM attraction a
            INNER JOIN attraction_type at2 ON at2.attraction_type_id = a.attraction_type
        """
        chat_gpt = RioAttractionML()
        chat_gpt.load_documents_from_sqlite_url(sqlite_url=DATABASE_URL,
                                                query=query)
        chat_gpt.build_chain()
        response = chat_gpt.generate_response(question)
        return response

    def build_trip_guide_day(self, response):
        # Regex para capturar as informações
        pattern = re.compile(
            r"Dia (\d{2}/\d{2}/\d{4}) \(([^)]+)\) - ([^-]+) - ([^-]+) "
            r"Descrição: (.*?) "
            r"Localização: (.*?) "
            r"Categoria de Atração: (.*?)$",
            re.DOTALL | re.MULTILINE
        )

        # Extraindo os dados
        resultados = pattern.findall(response)

        # Organização dos dados no objeto Day
        activities = {"morning": [], "afternoon": [], "evening": []}
        number_of_turns = 0
        days = []

        for match in resultados:
            print(number_of_turns)
            print(match)
            date, day_of_week, period, activity, description, location, category = match
            activity_details = {
                "name": activity.strip(),
                "location": location.strip(),
                "description": description.strip()
            }
            if period.lower() == "manhã":
                activities["morning"].append(activity_details)
            elif period.lower() == "tarde":
                activities["afternoon"].append(activity_details)
            elif period.lower() == "noite":
                activities["evening"].append(activity_details)

            number_of_turns += 1

            if number_of_turns == 3:
                date_obj = datetime.strptime(date, "%d/%m/%Y")
                day = Day(
                    date=date_obj,
                    day_of_week=day_of_week,
                    morning=activities["morning"],
                    afternoon=activities["afternoon"],
                    evening=activities["evening"]
                )
                days.append(day)
                number_of_turns = 0
                activities = {"morning": [], "afternoon": [], "evening": []}
        
        trip_guide_day = TripGuideDay("roteiro", days=days)
        return trip_guide_day
