import requests
import os
from dotenv import load_dotenv


load_dotenv()
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

class GoogleSheetData:

    def __init__(self):
        """ class to connect with the Google Sheet,
         when Google Sheet is empty, requests.get return 
         an empty list """

    def show_trips(self):
        """ return list of dicts from Sheet API """
        rersponce = requests.get(url=SHEET_ENDPOINT)
        trips_list = rersponce.json()["trips"]
        return trips_list


    def upload_result(self, sheet_dict:dict):
        """ Upload users data from interface """
        update_inputs = {
            "trip": sheet_dict
        }
        requests.post(url=SHEET_ENDPOINT, json=update_inputs)
