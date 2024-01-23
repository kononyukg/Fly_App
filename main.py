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

data_manager = DataManager(SHEET_ENDPOINT)
city_query_interface = CityQueryInterface(
        data_manager.upload_user_request, 
        YOUR_SHEET_URL)
iata_search = IataSearch(API_KEY, TEQ_LOCATION_API)
flight_data = FlightData(API_KEY, TEQ_SEARCH_API)


def send_feedback(message, departure_city, destination_city, url):
        """ Func to connect with notification_manager and 
        to send message and email """
        notification_manager = NotificationManager(message)
        notification_manager.send_message(
            ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER)
        notification_manager.send_email(
            YOUR_EMAIL_SMTP, YOUR_PASSWORD_SMTP, 
            departure_city, destination_city, url)


def check_prices(data):
    """ Check and add dates and prices to the Google Sheet, 
    then send SMS and Email """
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
        message_to_send = (f"Low price alert! Only {price} EUR to fly," 
                        f"\nfrom {city_from}-{airport_iata_from}"
                        f" to {city_to}-{airport_iata_to},"
                        f"\nfrom {date_to} to {date_back}.")
        send_feedback(message_to_send, city_from, city_to, deep_link)


def get_date_from_sheet():
    """ Connect and retutn date from the Google Sheet """
    try:
        sheet_data = data_manager.get_trips()
        return sheet_data
    except KeyError:
        title = "Error"
        message = ("You used the limit of 200 requests per month.")
        city_query_interface.show_error(title, message)


def get_iata_codes(sh_data):
    """ Update date from Google Sheet for IATA codes """
    for data in sh_data:
        if data["departureIataCode"] == "":
            departure_city = data["departureCity"]
            data["departureIataCode"] = iata_search.iata_for_city(departure_city)
        if data["destinationIataCode"] == "":
            destination_city = data["destinationCity"]
            data["destinationIataCode"] = iata_search.iata_for_city(destination_city)
    return sh_data
        

def find_flight(sh_data):
    """ Find flights with user's parameters """
    for data in sh_data:
        try:
            departure_iata = data["departureIataCode"]
            destination_iata = data["destinationIataCode"]
            trip_days = data["tripDays"]
            flight_data.search_fly(
                departure_iata, destination_iata, trip_days)
            check_prices(data)
            data_manager.update_sheet(sh_data)    
        except IndexError:
            title = "Sorry"
            message = ("There are no direct flights in this direction"
                       "\nPlease enter another destination city.")
            city_query_interface.show_eror(title, message)
            continue
    for data in sh_data:
        if  data["lowestPrice"] == "":
            row = data["id"]
            data_manager.delete_row(row)


def main():
    sheet_data = get_date_from_sheet()
    updated_sheet_data = get_iata_codes(sheet_data)
    find_flight(updated_sheet_data)

if __name__ == "__main__":
    main()
