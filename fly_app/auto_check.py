from google_sheet_data import GoogleSheetData
from search_flight_data import SearchFlightData
from message_manager import MessageManager
import os
from dotenv import load_dotenv


load_dotenv()
YOUR_EMAIL_SMTP = os.environ.get("YOUR_EMAIL_SMTP")
YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER")

google_sheet_data = GoogleSheetData()
search_flight_data = SearchFlightData()
message_manager = MessageManager()
sheet_data = google_sheet_data.show_trips()


def find_new_price():
    """ Check prices for all data in Google Sheet, 
    if it finds cheaper prices, will send email and edit data in Google Sheet """
    new_price = False
    for data in sheet_data:
        flight_dict = search_flight_data.flight_data_fron_teq(
            data['departureIataCode'], 
            data['destinationIataCode'], 
            data['tripDays']
            )
        if int(flight_dict['lowestPrice']) < int(data['lowestPrice']):
            new_price = True
            google_sheet_data.edit_sheet(flight_dict, data['id'])
            message_to_send = (f"Low price alert! Only {search_flight_data.price} EUR to fly," 
                                f"\nfrom {search_flight_data.departure_city}-{search_flight_data.departure_airport_code}"
                                f" to {search_flight_data.destination_city}-{search_flight_data.arrival_airport_code},"
                                f"\nfrom {search_flight_data.date_to_fly} to {search_flight_data.date_comeback_fly}.")
            message_manager.send_email(
                message_to_send, 
                YOUR_EMAIL_SMTP, 
                search_flight_data.departure_city, 
                search_flight_data.destination_city, 
                search_flight_data.deep_link
                )
    return new_price


def feed_back():
    """ Send sms """
    message = "There are no new search results."
    message_manager.send_message(YOUR_PHONE_NUMBER, message)


def recheck():
    """ Check the prices and send an sms if there are no cheaper prices """
    if find_new_price() == False:
        feed_back()


recheck()