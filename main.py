from dotenv import load_dotenv
import os
from city_query_interface import CityQueryInterface
from data_manager import DataManager
from iata_search import IataSearch
from flight_data import FlightData
from notification_manager import NotificationManager


load_dotenv()
TEQ_LOCATION_API = "https://api.tequila.kiwi.com/locations/query"
TEQ_SEARCH_API = "https://api.tequila.kiwi.com/v2/search"

SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
API_KEY = os.environ.get("API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER")
YOUR_EMAIL_SMTP = os.environ.get("YOUR_EMAIL_SMTP")
YOUR_PASSWORD_SMTP = os.environ.get("YOUR_PASSWORD_SMTP")
YOUR_SHEET_URL = os.environ.get("YOUR_SHEET_URL")


def main():
    """ Connect to the Google Sheet, run interface and add user requests,
    then get upgrade date from Google Sheet """
    data_manager = DataManager(SHEET_ENDPOINT)
    sheet_data = data_manager.sheet_for_run
    CityQueryInterface(
        sheet_data, data_manager.upload_user_request, 
        YOUR_SHEET_URL)
    sheet_data = data_manager.get_trips()


    """ Update date from Google Sheet for IATA codes """
    iata_search = IataSearch(API_KEY, TEQ_LOCATION_API)
    for data in sheet_data:
        if data["departureIataCode"] == "":
            departure_city = data["departureCity"]
            data["departureIataCode"] = iata_search.iata_for_city(departure_city)
        if data["destinationIataCode"] == "":
            destination_city = data["destinationCity"]
            data["destinationIataCode"] = iata_search.iata_for_city(destination_city)


    def send_feedback(message, departure_city, destination_city, url):
        """ Func to connect with notification_manager and 
        to send message and email """
        notification_manager = NotificationManager(message)
        notification_manager.send_message(
            ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER)
        notification_manager.send_email(
            YOUR_EMAIL_SMTP, YOUR_PASSWORD_SMTP, 
            departure_city, destination_city, url)
        

    """ Find flights with user's parameters """
    flight_data = FlightData(API_KEY, TEQ_SEARCH_API)
    for data in sheet_data:
        departure_iata = data["departureIataCode"]
        destination_iata = data["destinationIataCode"]
        trip_days = data["tripDays"]
        flight_data.search_fly(
            departure_iata, destination_iata, trip_days)
        """ Update Google Sheet for dates and prices from Flight_data 
        if there are lower then in Google Sheet or don't exist """
        if data["lowestPrice"] == "":
            data["lowestPrice"] = 0
        if flight_data.price < int(data["lowestPrice"]) or data["lowestPrice"] == 0:
            data["departureDate"] = flight_data.date_to_fly.split("T", 1)[0]
            data["returnDate"] = flight_data.date_comeback_fly.split("T", 1)[0]
            data["lowestPrice"] = flight_data.price
            price = data["lowestPrice"]
            city_from = data["departureCity"]
            airport_iata_from = flight_data.departure_airport_code
            city_to = data["destinationCity"]
            airport_iata_to = flight_data.arrival_airport_code
            date_to = data["departureDate"]
            date_back = data["returnDate"]
            deep_link = flight_data.deep_link
            message_to_send = (f"Low price alert! Only {price} euro to fly," 
                            f"\nfrom {city_from}-{airport_iata_from}"
                            f" to {city_to}-{airport_iata_to},"
                            f"\nfrom {date_to} to {date_back}.")
            send_feedback(message_to_send, city_from, city_to, deep_link)
            data_manager.update_sheet(sheet_data)


if __name__ == "__main__":
    main()
