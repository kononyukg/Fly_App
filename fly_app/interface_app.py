import webbrowser
from CTkMessagebox import CTkMessagebox
import customtkinter
import os
from search_flight_data import SearchFlightData
from google_sheet_data import GoogleSheetData
from message_manager import MessageManager
from dotenv import load_dotenv


load_dotenv()
YOUR_SHEET_URL = os.environ.get("YOUR_SHEET_URL")
YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER")
YOUR_EMAIL_SMTP = os.environ.get("YOUR_EMAIL_SMTP")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

search_flight_data = SearchFlightData()
google_sheet_data = GoogleSheetData()
message_manager = MessageManager()

class InterfaceApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.city_from = None
        self.city_to = None
        self.days = None
        google_sheet = google_sheet_data.show_trips()
        
        """ Window """
        self.title("Fly Alert")
        self.geometry("1100x1100")
        self.config(padx=20, pady=20)
        self.logo_label = customtkinter.CTkLabel(self, text="Please enter data of your trip", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=0, column=0, sticky="nsew", columnspan=3, padx=20, pady=(20, 5))
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        """ Table new data text """
        self.table_new_label = customtkinter.CTkLabel(self, text="New search request", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.table_new_label.grid(row=1, column=0, sticky="w", padx=30, pady=0)
        self.table_new = customtkinter.CTkTextbox(self, width=250, height=250, font=customtkinter.CTkFont(size=17, weight="bold"))
        self.table_new.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 20))

        """ Table with result """
        self.table_result_label = customtkinter.CTkLabel(self, text="Search result", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.table_result_label.grid(row=3, column=0, sticky="w", padx=30, pady=0)
        self.table_result = customtkinter.CTkTextbox(self,  width=250, height=250, font=customtkinter.CTkFont(size=17, weight="bold"))
        self.table_result.grid(row=4, column=0, sticky="nsew", padx=20, pady=(5, 20))

        """ Table sheet data text """
        self.table_data_label = customtkinter.CTkLabel(self, text="Google Sheet view", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.table_data_label.grid(row=1, column=1, sticky="w", padx=30, pady=0)
        self.table_data = customtkinter.CTkTextbox(self, width=250, height=450, font=customtkinter.CTkFont(size=17, weight="bold"))
        self.table_data.grid(row=2, column=1, rowspan=3, sticky="nsew", padx=20, pady=(5, 20))
        self.show_in_table(google_sheet)

        """ Table with SMS / Email buttons, entries """
        self.table_sms_email = customtkinter.CTkFrame(self, width=250, height=450)
        self.table_sms_email.grid(row=2, column=2, rowspan=3, sticky="nsew", padx=20, pady=(5, 20))
        self.table_sms_email.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.table_sms_email.columnconfigure(0, weight=1)

        """ Email interface """
        self.email_label = customtkinter.CTkLabel(self.table_sms_email, text="Your Email", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.email_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="S")
        self.email_entry = customtkinter.CTkEntry(self.table_sms_email, width=250, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.email_entry.grid(row=1, column=0, padx=5, pady=0)
        self.email_entry.insert(0, YOUR_EMAIL_SMTP)
        self.email_button = customtkinter.CTkButton(self.table_sms_email, text="SEND", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.send_email)
        self.email_button.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="N")

        """ SMS interface """
        self.sms_label = customtkinter.CTkLabel(self.table_sms_email, text="Your phone number", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sms_label.grid(row=3, column=0, padx=10, pady=(20, 10), sticky="S")
        self.sms_entry = customtkinter.CTkEntry(self.table_sms_email, width=250, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sms_entry.grid(row=4, column=0, padx=5, pady=0)
        self.sms_entry.insert(0, YOUR_PHONE_NUMBER)
        self.sms_button = customtkinter.CTkButton(self.table_sms_email, text="SEND", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.send_sms)
        self.sms_button.grid(row=5, column=0, padx=10, pady=(10, 20), sticky="N")

        """ Down Table with buttons, entries and labels"""
        self.table_interface = customtkinter.CTkFrame(self, width=900)
        self.table_interface.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        self.table_interface.columnconfigure((0, 1, 2), weight=1)
        
        """ Down Labels """
        self.city_from_label = customtkinter.CTkLabel(self.table_interface, text="Departure City:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_from_label.grid(row=0, column=0, padx=20, pady=30)
        self.city_to_label = customtkinter.CTkLabel(self.table_interface, text="Destination City:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_to_label.grid(row=1, column=0, padx=20, pady=30)
        self.how_many_days_label = customtkinter.CTkLabel(self.table_interface, text="Trip Days +-1:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.how_many_days_label.grid(row=2, column=0, padx=20, pady=30)

        """ Down Entries """
        self.city_from_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"), placeholder_text="Warsaw")
        self.city_from_entry.grid(row=0, column=1, padx=20, pady=30)
        self.city_to_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_to_entry.grid(row=1, column=1, padx=20, pady=30)
        self.how_many_days_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.how_many_days_entry.grid(row=2, column=1, padx=20, pady=30)
        
        """ Down Buttons """
        self.add_button = customtkinter.CTkButton(self.table_interface, text="ADD Data", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.add_user_data)
        self.add_button.grid(row=0, column=2, padx=20, pady=30)
        self.open_sheet_button = customtkinter.CTkButton(self.table_interface, text="Open Sheet", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.open_sheet)
        self.open_sheet_button.grid(row=1, column=2, padx=20, pady=30)
        self.search_button = customtkinter.CTkButton(self.table_interface, text="Let's search", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.search_fly)
        self.search_button.grid(row=2, column=2, padx=20, pady=30)

        
    def add_user_data(self):
        """ Take user request and put it in Table of new date """
        text_in_table = self.table_new.get("0.0", "end")
        """ if table_new is empty, method .get return 1 emty string, method len() return int 1 """
        if len(text_in_table) == 1:
            self.city_from = self.city_from_entry.get().title()
            self.city_to =  self.city_to_entry.get().title()
            self.days = self.how_many_days_entry.get()
            if len(self.city_from) == 0 or len(self.city_to) == 0 or len(self.days) == 0:
                CTkMessagebox(title="Information", message="ALL fields are required.")
            else:
                information = f"Departure City: {self.city_from}\nDestination City: {self.city_to}\nTrip Days: {self.days}\n\n"
                self.table_new.insert("0.0", f"{information}")
                self.city_to_entry.delete(0, "end")
                self.how_many_days_entry.delete(0, "end")
        else:
            CTkMessagebox(title="Information", message="The data has already been filled in,\nPerform a search.")

    def search_fly(self):
        """ Search iata codes for user request, then serch flight and if it successful 
        put in to Table data and Google Sheet """
        text_in_table = self.table_new.get("0.0", "end")
        if len(text_in_table) > 1:
            try:
                iata_city_from = search_flight_data.iata_for_city(self.city_from)
                iata_city_to = search_flight_data.iata_for_city(self.city_to)
                result_flight_dict = search_flight_data.flight_data_fron_teq(iata_city_from, iata_city_to, self.days)
                self.dict_to_table(result_flight_dict, self.table_result)
                self.table_new.delete("0.0", "end")
                google_sheet_data.upload_result(result_flight_dict)
            except IndexError:
                self.table_new.delete("0.0", "end")
                CTkMessagebox(title="Warning Message!", icon="warning", message="There are no direct flights in this direction"
                            "\nPlease enter another destination city.")
        else:
            CTkMessagebox(title="Warning Message!", icon="warning", message="You need to add data for the search.")

    def dict_to_table(self, sheet_dict, which_table):
        """ Take dict and put it in interface """
        city_from = sheet_dict['departureCity']
        iata_from = sheet_dict['departureIataCode']
        city_to = sheet_dict['destinationCity']
        iata_to = sheet_dict['destinationIataCode']
        date_from = sheet_dict['departureDate']
        date_back = sheet_dict['returnDate']
        days = sheet_dict['tripDays']
        cost = sheet_dict['lowestPrice']
        which_table.insert("0.0", f"Departure City:   {city_from}\n"
                               f"Departure Iata Code:   {iata_from}\n"
                               f"Destination City:   {city_to}\n"
                               f"Destination Iata Code:   {iata_to}\n"
                               f"Departure Date:   {date_from}\n"
                               f"Return Date:   {date_back}\n"
                               f"Trip Days:   {days}\n"
                               f"Lowest Price:   {cost}\n\n")
        
    def show_in_table(self, sheet):
        """ Take google sheet and open it in table interface """
        for data in sheet:
            self.dict_to_table(data, self.table_data)

    def open_sheet(self):
        webbrowser.open(YOUR_SHEET_URL)

    def send_sms(self):
        you_phone_number = self.sms_entry.get()
        message_to_send = (f"Low price alert! Only {search_flight_data.price} EUR to fly," 
                            f"\nfrom {search_flight_data.departure_city}-{search_flight_data.departure_airport_code}"
                            f" to {search_flight_data.destination_city}-{search_flight_data.arrival_airport_code},"
                            f"\nfrom {search_flight_data.date_to_fly} to {search_flight_data.date_comeback_fly}.")
        message_manager.send_message(you_phone_number, message_to_send)

    def send_email(self):
        message_to_send = (f"Low price alert! Only {search_flight_data.price} EUR to fly," 
                            f"\nfrom {search_flight_data.departure_city}-{search_flight_data.departure_airport_code}"
                            f" to {search_flight_data.destination_city}-{search_flight_data.arrival_airport_code},"
                            f"\nfrom {search_flight_data.date_to_fly} to {search_flight_data.date_comeback_fly}.")
        you_email = self.email_entry.get()
        departure_city = search_flight_data.departure_city
        destination_city = search_flight_data.destination_city
        url = search_flight_data.deep_link
        message_manager.send_email(message_to_send, you_email, departure_city, destination_city, url)
