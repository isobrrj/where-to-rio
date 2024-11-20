class TripGuideBuilder:
    def __init__(self, tourism_preference) -> None:
        self.tourism_preference = tourism_preference

    def build_question_message_llm(self):
        str_question = f"Quais pontos turisticos posso visitar, durante minha viagem, entre o dia {self.tourism_preference.init_date} e {self.tourism_preference.end_date} no Rio de Janeiro? Estarei hospedado no bairro {self.tourism_preference.neigh} e tenho preferência por "
        for k in self.tourism_preference.preferences:
            if self.tourism_preference.preferences[k]:
                str_question += f" {k},"
        str_question = str_question[:-1] + "."
        return str_question
