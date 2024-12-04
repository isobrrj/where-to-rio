class Day:
    """
    Representa um dia no roteiro, com atividades divididas por períodos.
    """
    def __init__(self, date, day_of_week, breakfast=None, morning=None, lunch=None, afternoon=None, evening=None, dinner=None):
        """
        Inicializa um dia do roteiro.
        
        :param date: A data do dia (string ou objeto datetime).
        :param day_of_week: O dia da semana (string, ex: "Segunda-feira").
        :param breakfast: Atividade planejada para o café da manhã.
        :param morning: Lista de atividades planejadas para a manhã.
        :param lunch: Atividade planejada para o almoço.
        :param afternoon: Lista de atividades planejadas para a tarde.
        :param evening: Lista de atividades planejadas para a noite.
        :param dinner: Atividade planejada para o jantar.
        """
        
        self.date = date
        self.day_of_week = day_of_week
        self.breakfast = breakfast
        self.morning = morning if morning else []
        self.lunch = lunch
        self.afternoon = afternoon if afternoon else []
        self.dinner = dinner
        self.evening = evening if evening else []
        

    def add_morning_activity(self, activity):
        """
        Adiciona uma atividade ao período da manhã.
        :param activity: A atividade a ser adicionada.
        """
        self.morning.append(activity)

    def add_afternoon_activity(self, activity):
        """
        Adiciona uma atividade ao período da tarde.
        :param activity: A atividade a ser adicionada.
        """
        self.afternoon.append(activity)

    def add_evening_activity(self, activity):
        """
        Adiciona uma atividade ao período da noite.
        :param activity: A atividade a ser adicionada.
        """
        self.evening.append(activity)

    def __str__(self):
        """
        Retorna uma representação em string do dia e suas atividades.
        """
        morning_str = "\n    - ".join(self.morning) if self.morning else "Nenhuma atividade"
        afternoon_str = "\n    - ".join(self.afternoon) if self.afternoon else "Nenhuma atividade"
        evening_str = "\n    - ".join(self.evening) if self.evening else "Nenhuma atividade"
        return (
            f"Data: {self.date} ({self.day_of_week})\n"
            f"  Café da Manhã: {self.breakfast or 'Nenhuma atividade'}\n"
            f"  Manhã:\n    - {morning_str}\n"
            f"  Almoço: {self.lunch or 'Nenhuma atividade'}\n"
            f"  Tarde:\n    - {afternoon_str}\n"
            f"  Noite:\n    - {evening_str}\n"
            f"  Jantar: {self.dinner or 'Nenhuma atividade'}"
        )


class TripGuideDay:
    """
    Representa um roteiro de viagem composto por vários dias.
    """
    def __init__(self, name, days=None):
        """
        Inicializa o roteiro de viagem.

        :param name: O nome do roteiro de viagem.
        """
        self.name = name
        self.days = [] if not days else days  # Lista de objetos Day

    def add_day(self, day):
        """
        Adiciona um objeto Day ao roteiro.

        :param day: Um objeto Day.
        """
        if isinstance(day, Day):
            self.days.append(day)
        else:
            raise ValueError("O objeto deve ser uma instância da classe Day.")

    def generate_data(self):
        """
        Gera uma visualização em string de todos os dias no roteiro.
        """
        return "\n\n".join(str(day) for day in self.days)

    def __str__(self):
        """
        Retorna uma representação em string do roteiro de viagem.
        """
        days_str = self.generate_data() if self.days else "Nenhum dia adicionado."
        return f"Roteiro: {self.name}\n\n{days_str}"
