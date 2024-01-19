import smtplib
from twilio.rest import Client

""" twilio doesnt work with Python 3.12, try 3.9-3.10 """


class NotificationManager:
    def __init__(self, message_to_send):
        """ Class to connect with the Twilio, SMTP and send a message """
        self.message_to_send = message_to_send

    def send_message(self, account_sid, auth_token, twilio_phone_number, you_phone_number):
        """ Sending SMS with trips """
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body=self.message_to_send,
                from_=twilio_phone_number,
                to=you_phone_number,
            )
        print(message.status)

    
    def send_email(self, you_email_smtp, you_password_smtp,departure_city, destination_city, url):
        """ Sending email with trips """
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=you_email_smtp, password=you_password_smtp)
            connection.sendmail(
                from_addr=you_email_smtp,
                to_addrs=you_email_smtp,
                msg=f"Subject:Trip from {departure_city} to {destination_city}!\n\n{ self.message_to_send}\nlink:{url}"
            )
            