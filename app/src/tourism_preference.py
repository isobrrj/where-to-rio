class TourismPreference:
    def __init__(self, neigh, init_date, end_date, preferences) -> None:
        self.neigh = neigh
        self.init_date = init_date
        self.end_date = end_date
        self.preferences = preferences

    def build_message(self):
        str_question = f"Quais pontos turisticos posso visitar, durante minha viagem, entre o dia {self.init_date} e {self.end_date} no Rio de Janeiro? Estarei hospedado no bairro {self.neigh} e tenho preferência por "
        for k, v in self.preferences:
            if self.preferences[k]:
                str_question += f" {k} "
        str_question += "."
        return str_question
