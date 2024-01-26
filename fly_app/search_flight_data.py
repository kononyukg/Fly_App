import requests
import os 
import datetime
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.environ.get("API_KEY")
TEQ_LOCATION_API = "https://api.tequila.kiwi.com/locations/query"
TEQ_SEARCH_API = "https://api.tequila.kiwi.com/v2/search"


class SearchFlightData:
    
    def __init__(self):
        """ Class to connect with the Tequila API """
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.tomorrow = tomorrow_date.strftime("%d/%m/%Y")
        four_months_date = tomorrow_date + datetime.timedelta(days=30*4)
        self.four_months = four_months_date.strftime("%d/%m/%Y")
        self.departure_airport_code = None
        self.departure_city = None
        self.departure_iata = None
        self.destination_city = None
        self.destination_iata = None
        self.arrival_airport_code = None
        self.date_to_fly = None
        self.date_comeback_fly = None
        self.deep_link = None
        self.nights_in_destination = None
        self.price = None

    def iata_for_city(self, city):
        """ Take name of city and return IATA code """
        headers = {
           "apikey": API_KEY
        }
        parameters = {
            "term": city,
            "location_types": "city"
        }
        iata_code = requests.get(
            url=TEQ_LOCATION_API,
            params=parameters,
            headers=headers
        ).json()["locations"][0]["code"]
        return iata_code
    
    def flight_data_fron_teq(self, departure_iata, destination_iata, trip_days) -> dict:
        """ Take Departure IATA Code, Destination IATA Code, Trip Days
        and find flights, then upgrade attributes """
        self.departure_iata = departure_iata
        self.destination_iata = destination_iata
        self.nights_in_destination = int(trip_days)
        headers = {
            "apikey": API_KEY
        }
        parameters = {
            "fly_from": self.departure_iata,
            "fly_to": self.destination_iata,
            "date_from": self.tomorrow,
            "date_to": self.four_months,
            "nights_in_dst_from": self.nights_in_destination - 1,
            "nights_in_dst_to": self.nights_in_destination + 1,
            "max_stopovers": 0,
            "limit": 1,
            "curr": "EUR",
        }
        result = requests.get(
            url=TEQ_SEARCH_API,
            params=parameters, headers=headers).json()["data"][0]
        self.departure_airport_code = result["flyFrom"]
        self.departure_city = result["cityFrom"]
        self.arrival_airport_code = result["flyTo"]
        self.destination_city = result["cityTo"]
        self.date_to_fly = result["local_departure"].split("T", 1)[0]
        self.date_comeback_fly = result["route"][1]["utc_departure"].split("T", 1)[0]
        self.price = result["price"]
        self.deep_link = result["deep_link"]
        sheet_dict = {
            'departureCity': self.departure_city, 
            'departureIataCode': self.departure_iata, 
            'destinationCity':  self.destination_city, 
            'destinationIataCode': self.destination_iata, 
            'departureDate': self.date_to_fly, 
            'returnDate': self.date_comeback_fly, 
            'tripDays': self.nights_in_destination, 
            'lowestPrice': f"{self.price} EUR", 
            }
        return sheet_dict
