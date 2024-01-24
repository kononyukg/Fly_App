from tkinter import *
import webbrowser
from tkinter import messagebox
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class CityQueryInterface(customtkinter.CTk):
    def __init__(self, funk_to_upload, sheet_url, funk_to_start):
        super().__init__()
        self.sheet_url = sheet_url
        self.funk_to_upload = funk_to_upload
        self.funk_to_start = funk_to_start
        self.sheet_list = [
                {
                    'departureCity': '', 
                    'departureIataCode': '', 
                    'destinationCity': '', 
                    'destinationIataCode': '', 
                    'departureDate': '', 
                    'returnDate': '', 
                    'tripDays': '', 
                    'lowestPrice': '', 
                    'id': ''
                    }
                ]
        
        """ Window """
        self.title("Fly Alert")
        self.geometry("1000x920")
        self.config(padx=20, pady=20)
        self.logo_label = customtkinter.CTkLabel(self, text="Please enter data of your trip", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 5))
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(0, weight=1)

        """ Table sheet data text """
        self.table_data_label = customtkinter.CTkLabel(self, text="Data from Google Sheet", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.table_data_label.grid(row=1, column=0, sticky="w", padx=30, pady=0)
        self.table_data = customtkinter.CTkTextbox(self, width=900)
        self.table_data.grid(row=2, column=0, sticky="nsew", padx=30, pady=(5, 20))

        """ Table new data text """
        self.table_new_label = customtkinter.CTkLabel(self, text="New user date", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.table_new_label.grid(row=3, column=0, sticky="w", padx=30, pady=0)
        self.table_new = customtkinter.CTkTextbox(self, width=900)
        self.table_new.grid(row=4, column=0, sticky="nsew", padx=30, pady=(5, 20))

        """ Table with buttons, entries and labels"""
        self.table_interface = customtkinter.CTkFrame(self, width=900)
        self.table_interface.grid(row=5, column=0, sticky="nsew", padx=30, pady=20)
        self.table_interface.columnconfigure((0, 1, 2), weight=1)
        
        """ Labels """
        self.city_from_label = customtkinter.CTkLabel(self.table_interface, text="Departure City:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_from_label.grid(row=0, column=0, padx=20, pady=30)
        self.city_to_label = customtkinter.CTkLabel(self.table_interface, text="Destination City:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_to_label.grid(row=1, column=0, padx=20, pady=30)
        self.how_many_days_label = customtkinter.CTkLabel(self.table_interface, text="Trip Days +-1:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.how_many_days_label.grid(row=2, column=0, padx=20, pady=30)

        """ Entries """
        self.city_from_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"), placeholder_text="Gdansk")
        self.city_from_entry.grid(row=0, column=1, padx=20, pady=30)
        self.city_to_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.city_to_entry.grid(row=1, column=1, padx=20, pady=30)
        self.how_many_days_entry = customtkinter.CTkEntry(self.table_interface, width=250, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.how_many_days_entry.grid(row=2, column=1, padx=20, pady=30)
        
        """ Buttons """
        self.add_button = customtkinter.CTkButton(self.table_interface, text="ADD Data", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.add_user_data)
        self.add_button.grid(row=0, column=2, padx=20, pady=30)
        self.open_sheet_button = customtkinter.CTkButton(self.table_interface, text="Open Sheet", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.go_to_sheet)
        self.open_sheet_button.grid(row=1, column=2, padx=20, pady=30)
        self.search_button = customtkinter.CTkButton(self.table_interface, text="Let's search", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.funk_to_start)
        self.search_button.grid(row=2, column=2, padx=20, pady=30)
        
    def add_user_data(self):
        """ Command for button to add user data in Google Sheet """
        city_from = self.city_from_entry.get().title()
        city_to =  self.city_to_entry.get().title()
        days = self.how_many_days_entry.get()
        if len(city_from) == 0 or len(city_to) == 0 or len(days) == 0:
            title = "Information"
            message = "ALL fields are required"
            messagebox.showinfo(title=title, message=message)
        else:
            self.funk_to_upload(self.sheet_list, city_from, city_to, days)
            information = f"Departure City: {city_from}\nDestination City: {city_to}\nTrip Days: {days}\n\n"
            self.table_new.insert("0.0", f"{information}")
            self.city_to_entry.delete(0, "end")
            self.how_many_days_entry.delete(0, "end")

    def go_to_sheet(self):
        webbrowser.open(self.sheet_url)

    def show_error(self, title_error, message_error):
        messagebox.showinfo(title=title_error, message=message_error)

    def sheet_to_table(self, data):
        """ Take data from Google sheet and show it in interface """
        city_from = data['departureCity']
        iata_from = data['departureIataCode']
        city_to = data['destinationCity']
        iata_to = data['destinationIataCode']
        date_from = data['departureDate']
        date_back = data['returnDate']
        days = data['tripDays']
        cost = data['lowestPrice']
        id = data['id']
        self.table_data.insert("0.0", f"Departure City:   {city_from}\n"
                               f"Departure Iata Code:   {iata_from}\n"
                               f"Destination City:   {city_to}\n"
                               f"Destination Iata Code:   {iata_to}\n"
                               f"Departure Date:   {date_from}\n"
                               f"Return Date:   {date_back}\n"
                               f"Trip Days:   {days}\n"
                               f"Lowest Price:   {cost}\n"
                               f"Id:   {id}\n\n")
