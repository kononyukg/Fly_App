import requests


class DataManager:

    def __init__(self, sheet_endpoint):
        """ class to connect with the Google Sheet,
         when Google Sheet is empty, requests.get return 
         an empty list """
        self.sheet_data = None
        self.sheet_endpoint = sheet_endpoint
        self.response_sheet = None

    def get_trips(self):
        """ return list of dicts from Sheet API """
        self.response_sheet = requests.get(url=self.sheet_endpoint)
        trips_list = self.response_sheet.json()["trips"]
        return trips_list

    def update_sheet(self, sheet_data):
        """ update list of dict """
        self.sheet_data = sheet_data
        for row in self.sheet_data:
            update_url = f"{self.sheet_endpoint}/{row['id']}"
            update_inputs = {
                "trip": {
                    "departureIataCode": row["departureIataCode"],
                    "destinationIataCode": row["destinationIataCode"],
                    "departureDate": row["departureDate"],
                    "returnDate": row["returnDate"],
                    "lowestPrice": row["lowestPrice"]
                }
            }
            requests.put(url=update_url, json=update_inputs)

    def upload_user_request(self, sheet_data, departure_city, destination_city, trip_days):
        """ upload users data from interface """
        self.sheet_data = sheet_data
        for row in self.sheet_data:
            update_url = self.sheet_endpoint
            update_inputs = {
                "trip": {
                    "departureCity": departure_city,
                    "destinationCity": destination_city,
                    "tripDays": trip_days,
                }
            }
            requests.post(url=update_url, json=update_inputs)

    def delete_row(self, row_id):
         update_url = f"{self.sheet_endpoint}/{row_id}"
         requests.delete(url=update_url)
