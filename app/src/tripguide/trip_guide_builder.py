from chat_gpt.rio_attraction_ml import RioAttractionML
from tripguide.trip_guide import Day, TripGuideDay
import json
from datetime import datetime
from database.config import DATABASE_URL


class TripGuideBuilder:
    def __init__(self, tourism_preference, chat_gpt_ai) -> None:
        self.tourism_preference = tourism_preference
        self.chat_gpt = chat_gpt_ai

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
                at2.attraction_type AS "Categoria de Atração"
            FROM attraction a
            INNER JOIN attraction_type at2 ON at2.attraction_type_id = a.attraction_type
        """
        self.chat_gpt.load_documents_from_sqlite_url(sqlite_url=DATABASE_URL,
                                                     query=query)
        self.chat_gpt.build_chain()
        response = self.chat_gpt.generate_response(question)
        return response

    def build_trip_guide_day(self, response):
        resp_json = json.loads(response)

        activities = {"morning": [], "afternoon": [], "evening": []}
        number_of_turns = 0
        days = []

        for match in resp_json[list(resp_json.keys())[0]]:
            activity_details = {
                "name": match["Atração"].strip(),
                "location": match["Descrição"].strip(),
                "description": match["Localização"].strip()
            }
            period = match["Turno"].lower()
            date = match["Data"]
            day_of_week = match["Dia da Semana"]

            if period == "manhã":
                activities["morning"].append(activity_details)
            elif period == "tarde":
                activities["afternoon"].append(activity_details)
            elif period == "noite":
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
