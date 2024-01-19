from dotenv import load_dotenv
import os
from city_query_interface import CityQueryInterface
from data_manager import DataManager
from iata_search import IataSearch
from flight_data import FlightData
from notification_manager import NotificationManager


load_dotenv()
SHEET_ENDPOINT = "https://api.sheety.co/0e464314f559102cd39908af539f4adf/myTrips/trips"
TEQ_LOCATION_API = "https://api.tequila.kiwi.com/locations/query"
TEQ_SEARCH_API = "https://api.tequila.kiwi.com/v2/search"

API_KEY = os.environ.get("API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER")
YOUR_EMAIL_SMTP =  os.environ.get("YOUR_EMAIL_SMTP")
YOUR_PASSWORD_SMTP =  os.environ.get("YOUR_PASSWORD_SMTP")


""" Connect to the Google Sheet, run interface and add user requests,
then get whole date from Google Sheet """
data_manager = DataManager(SHEET_ENDPOINT)
sheet_data = data_manager.sheet_for_run
city_query_interface = CityQueryInterface(sheet_data, data_manager.upload_user_request)
sheet_data = data_manager.get_trips()


""" Update Google Sheet for IATA codes """
iata_search = IataSearch(API_KEY, TEQ_LOCATION_API)
for data in sheet_data:
    if data["departureIataCode"] == "":
        departure_city = data["departureCity"]
        data["departureIataCode"] = iata_search.iata_for_city(departure_city)
    if data["destinationIataCode"] == "":
        destination_city = data["destinationCity"]
        data["destinationIataCode"] = iata_search.iata_for_city(destination_city)
data_manager.update_sheet(sheet_data)


""" Find flights and update Google Sheet for dates and prices """
flight_data = FlightData(API_KEY, TEQ_SEARCH_API)
for data in sheet_data:
    departure_iata = data["departureIataCode"]
    destination_iata = data["destinationIataCode"]
    trip_days = data["tripDays"]
    search_data = flight_data.search_fly(departure_iata, destination_iata, trip_days)
    data["departureDate"] = flight_data.date_to_fly.split("T", 1)[0]
    data["returnDate"] = flight_data.date_comeback_fly.split("T", 1)[0]
    data["lowestPrice"] = flight_data.price
data_manager.update_sheet(sheet_data)
            

# def main():
    
#     # data_manager.update_sheet(sheet_data)
#     # send_feedback()


# if __name__ == "__main__":
#     main()
