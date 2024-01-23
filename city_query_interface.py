from tkinter import *
import webbrowser
from tkinter import messagebox

FONT = ("Arial", 20, "bold")
COLOR = "#C5FFF8"
YOUR_CITY = "Gdansk"

class CityQueryInterface():

    def __init__(self, funk_to_upload, sheet_url):
        """ Window """
        self.sheet_url = sheet_url
        self.funk_to_upload = funk_to_upload
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
        self.window = Tk()
        self.window.title("Fly Alert")
        self.window.config(padx=50, pady=50, bg="#C5FFF8")
        self.canvas = Canvas(width=600, height=500, bg=COLOR, highlightthickness=0)
        self.plane_img = PhotoImage(file="img/plane.png")
        self.canvas.create_image(300, 250, image=self.plane_img)
        self.canvas.create_text(
            290, 
            150, 
            text="Please enter\n the request",  
            font=("Arial", 50, "bold"), fill="black"
            )
        self.canvas.grid(row=0, column=0, columnspan=3)
        """ Labels """
        self.city_from_label = Label(text="From City:", font=FONT, bg=COLOR)
        self.city_from_label.grid(row=1, column=0)
        self.city_to_label = Label(text="To City:", font=FONT, bg=COLOR)
        self.city_to_label.grid(row=2, column=0)
        self.how_many_days_label = Label(text="How long:", font=FONT, bg=COLOR)
        self.how_many_days_label.grid(row=3, column=0)
        """ Entries """
        self.city_from_entry = Entry(width=12, font=FONT)
        self.city_from_entry.grid(row=1, column=1)
        self.city_from_entry.insert(0, YOUR_CITY)
        self.city_from_entry.focus()
        self.city_to_entry = Entry(width=12, font=FONT)
        self.city_to_entry.grid(row=2, column=1)
        self.how_many_days_entry = Entry(width=12, font=FONT)
        self.how_many_days_entry.grid(row=3, column=1)
        """ Buttons """
        self.city_from_button = Button(text="ADD Data", font=FONT, width=12, command=self.add_user_data)
        self.city_from_button.grid(row=1,column=2)
        self.go_to_sheet_button = Button(text="Open Sheet", font=FONT, width=12, command=self.go_to_sheet)
        self.go_to_sheet_button.grid(row=3,column=2)

        self.window.mainloop()
        
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
            self.city_from_entry.delete(0, "end")
            self.city_to_entry.delete(0, "end")
            self.how_many_days_entry.delete(0, "end")
            self.city_from_entry.insert(0, YOUR_CITY)

    def go_to_sheet(self):
        webbrowser.open(self.sheet_url)

    def show_eror(self, title_eror, message_eror):
        messagebox.showinfo(title=title_eror, message=message_eror)
