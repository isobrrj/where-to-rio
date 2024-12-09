from urllib.parse import urlencode

class TravelRoutes:
    def __init__(self, origin: str, destination: str):
        self.origin = origin
        self.destination = destination

    def generate_travel_route(self):
        base_url = "https://www.google.com/maps/dir/"
        params={
            "api": 1,
            "origin": self.origin,
            "destination": self.destination
        }

        return f"{base_url}?{urlencode(params)}"