import datetime
import requests


class FlightData:
    def __init__(self, api_key, teq_search_api):
        """ class to connect with the Flight Search API """
        self.teq_search_api = teq_search_api
        self.api_key = api_key
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.tomorrow = tomorrow_date.strftime("%d/%m/%Y")
        six_months_date = tomorrow_date + datetime.timedelta(days=30*4)
        self.six_months = six_months_date.strftime("%d/%m/%Y")
        self.result = None
        self.city_to_fly = None
        self.price = None
        self.departure_airport_code = None
        self.departure_city = None
        self.arrival_city = None
        self.arrival_airport_code = None
        self.date_to_fly = None
        self.date_comeback_fly = None
        self.booking_token = None

    def search_fly(self, departure_iata, destination_iata, trip_days):
        """ Take Departure IATA Code, Destination IATA Code, Trip Days
        and find flights, then upgrade attributes """
        self.city_fly_from = departure_iata
        self.city_fly_to = destination_iata
        self.nights_in_destination = int(trip_days)
        headers = {
            "apikey": self.api_key
        }
        parameters = {
            "fly_from": self.city_fly_from,
            "fly_to": self.city_fly_to,
            "date_from": self.tomorrow,
            "date_to": self.six_months,
            "nights_in_dst_from": self.nights_in_destination - 1,
            "nights_in_dst_to": self.nights_in_destination + 1,
            "max_stopovers": 0,
            "limit": 1,
            "curr": "EUR",
        }
        self.result = requests.get(
            url=self.teq_search_api,
            params=parameters, headers=headers).json()["data"][0]
        self.price = self.result["price"]
        self.departure_airport_code = self.result["flyFrom"]
        self.departure_city = self.result["cityFrom"]
        self.arrival_airport_code = self.result["flyTo"]
        self.arrival_city = self.result["cityTo"]
        self.date_to_fly = self.result["local_departure"]
        self.date_comeback_fly = self.result["route"][1]["utc_departure"]
        self.deep_link = self.result["deep_link"]
