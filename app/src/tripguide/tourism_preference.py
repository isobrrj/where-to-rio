class TourismPreference:
    def __init__(self, neigh: str,
                 init_date: str,
                 end_date: str,
                 attr_preferences: dict,
                 lunch_preferences: dict,
                 budget: str) -> None:
        self.neigh = neigh
        self.init_date = init_date
        self.end_date = end_date
        self.attr_preferences = attr_preferences
        self.lunch_preferences = lunch_preferences
        self.budget = budget