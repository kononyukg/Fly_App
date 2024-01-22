import requests


class IataSearch:
    
    def __init__(self, api_key, teq_location_api):
        """ Class to connect with the Flight Locations API """
        self.city = None
        self.teq_location_api = teq_location_api
        self.api_key = api_key

    def iata_for_city(self, city_name):
        """ Take name of city and search iata code for it """
        self.city = city_name
        headers = {
           "apikey": self.api_key
        }
        parameters = {
            "term": self.city,
            "location_types": "city"
        }
        iata_code = requests.get(
            url=self.teq_location_api,
            params=parameters,
            headers=headers
        ).json()["locations"][0]["code"]
        return iata_code
