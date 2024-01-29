import smtplib
from twilio.rest import Client
import os 
from dotenv import load_dotenv


load_dotenv()
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER")
YOUR_EMAIL_SMTP = os.environ.get("YOUR_EMAIL_SMTP")
YOUR_PASSWORD_SMTP = os.environ.get("YOUR_PASSWORD_SMTP")

class MessageManager:
    
    def __init__(self):
        """ Class to connect with the Twilio, SMTP and send a message """

    def send_message(self, you_phone_number, message_to_send):
        """ Sending SMS with trips """
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
                body=message_to_send,
                from_=TWILIO_PHONE_NUMBER,
                to=you_phone_number,
            )
        print(message.status)

    def send_email(self, message_to_send, you_email, departure_city, destination_city, url):
        """ Sending email with trips and url"""
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=YOUR_EMAIL_SMTP, password=YOUR_PASSWORD_SMTP)
            connection.sendmail(
                from_addr=YOUR_EMAIL_SMTP,
                to_addrs=you_email,
                msg=(f"Subject:Trip from {departure_city} to "f"{destination_city}!\n\n{message_to_send}\nlink:{url}").encode("utf-8")
            )
