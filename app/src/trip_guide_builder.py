class TripGuideBuilder:
    def __init__(self, tourism_preference) -> None:
        self.tourism_preference = tourism_preference

    def build_question_message_llm(self):
        str_question = f"Irei conhecer o Rio de Janeiro entre o dia {self.tourism_preference.init_date} e {self.tourism_preference.end_date}. Estarei hospedado no bairro {self.tourism_preference.neigh} e tenho preferência por conhecer atrações nas seguintes categorias: "
        for k in self.tourism_preference.attr_preferences:
            if self.tourism_preference.attr_preferences[k]:
                str_question += f" {k},"
        str_question = str_question[:-1] + "."
        str_question = str_question + " Além disso, quero comer em restaurantes das seguintes categorias: "
        for k in self.tourism_preference.lunch_preferences:
            if self.tourism_preference.lunch_preferences[k]:
                str_question += f" {k},"
        str_question = str_question[:-1] + "."
        str_question = str_question + f" Minha categoria de gasto na alimentação é, no máximo, {self.tourism_preference.budget}."
        str_question = str_question + " Que pontos turísticos e restaurantes poderia conhecer durante minha estadia?"
        return str_question
