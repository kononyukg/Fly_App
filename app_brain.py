from dotenv import load_dotenv
import os
from city_query_interface import CityQueryInterface
from data_manager import DataManager
from iata_search import IataSearch
from flight_data import FlightData
from notification_manager import NotificationManager
import threading


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


class AppBrain:

    def __init__(self):
        self.data_manager = DataManager(SHEET_ENDPOINT)
        self.city_query_interface = CityQueryInterface(
                self.data_manager.upload_user_request, 
                YOUR_SHEET_URL, self.run_code_search_flights)
        self.iata_search = IataSearch(API_KEY, TEQ_LOCATION_API)
        self.flight_data = FlightData(API_KEY, TEQ_SEARCH_API)
        self.show_in_iterface()
    
    def show_in_iterface(self):
        data_to_interface = self.data_manager.get_trips()
        for data in data_to_interface:
            if len(data_to_interface) == 0:
                pass
            else:
                try:
                    self.city_query_interface.sheet_to_table(data)
                except:
                    continue

    def send_feedback(self, message, departure_city, destination_city, url):
            """ Func to connect with notification_manager and 
            to send message and email """
            self.notification_manager = NotificationManager(message)
            self.notification_manager.send_message(
                ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER)
            self.notification_manager.send_email(
                YOUR_EMAIL_SMTP, YOUR_PASSWORD_SMTP, 
                departure_city, destination_city, url)
            
    def check_prices(self, data):
        """ Check and add dates and prices to the Google Sheet, 
        then send SMS and Email """
        if data["lowestPrice"] == "":
            data["lowestPrice"] = 0
        if self.flight_data.price < int(data["lowestPrice"]) or data["lowestPrice"] == 0:
            data["departureDate"] = self.flight_data.date_to_fly.split("T", 1)[0]
            data["returnDate"] = self.flight_data.date_comeback_fly.split("T", 1)[0]
            data["lowestPrice"] = self.flight_data.price
            price = data["lowestPrice"]
            city_from = data["departureCity"]
            airport_iata_from = self.flight_data.departure_airport_code
            city_to = data["destinationCity"]
            airport_iata_to = self.flight_data.arrival_airport_code
            date_to = data["departureDate"]
            date_back = data["returnDate"]
            deep_link = self.flight_data.deep_link
            message_to_send = (f"Low price alert! Only {price} EUR to fly," 
                            f"\nfrom {city_from}-{airport_iata_from}"
                            f" to {city_to}-{airport_iata_to},"
                            f"\nfrom {date_to} to {date_back}.")
            self.send_feedback(message_to_send, city_from, city_to, deep_link)

    def get_date_from_sheet(self):
        """ Connect and retutn date from the Google Sheet """
        try:
            sheet_data = self.data_manager.get_trips()
            return sheet_data
        except KeyError:
            title = "Error"
            message = ("You used the limit of 200 requests per month.")
            self.city_query_interface.show_error(title, message)

    def get_iata_codes(self, sh_data):
        """ Update date from Google Sheet for IATA codes """
        for data in sh_data:
            if data["departureIataCode"] == "":
                departure_city = data["departureCity"]
                data["departureIataCode"] = self.iata_search.iata_for_city(departure_city)
            if data["destinationIataCode"] == "":
                destination_city = data["destinationCity"]
                data["destinationIataCode"] = self.iata_search.iata_for_city(destination_city)
        return sh_data
            
    def find_flight(self, sh_data):
        """ Find flights with user's parameters """
        for data in sh_data:
            try:
                departure_iata = data["departureIataCode"]
                destination_iata = data["destinationIataCode"]
                trip_days = data["tripDays"]
                self.flight_data_search_fly_thread = threading.Thread(
                    target=self.flight_data.search_fly,
                    args=(departure_iata, destination_iata, trip_days,)
                    )
                self.flight_data_search_fly_thread.start()
                self.flight_data_search_fly_thread.join()
                self.check_prices_thread = threading.Thread(
                    target=self.check_prices,
                    args=(data,)
                    )
                self.check_prices_thread.start()
                self.check_prices_thread.join()
                self.data_manager_update_sheet_thread = threading.Thread(
                    target=self.data_manager.update_sheet,
                    args=(sh_data,)
                )
                self.data_manager_update_sheet_thread.start()
                self.data_manager_update_sheet_thread.join()     
            except IndexError:
                title = "Sorry"
                message = ("There are no direct flights in this direction"
                        "\nPlease enter another destination city.")
                self.city_query_interface.show_error(title, message)
                continue
        for data in sh_data:
            if  data["lowestPrice"] == "":
                row = data["id"]
                self.data_manager.delete_row(row)

    def run_code_search_flights(self):
        """ Run code when you tap 'search' in interface """
        self.city_query_interface.table_data.delete("0.0", "end")
        self.city_query_interface.table_new.delete("0.0", "end")
        sheet_data = self.get_date_from_sheet()
        updated_sheet_data = self.get_iata_codes(sheet_data)
        self.find_flight_thread = threading.Thread(
            target=self.find_flight,
            args=(updated_sheet_data,)
        )
        self.find_flight_thread.start()
        self.find_flight_thread.join() 
        self.show_in_iterface()
