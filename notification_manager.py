from twilio.rest import Client
""" twilio doesnt work with Python 3.12, try 3.9-3.10 """


class NotificationManager:
    def __init__(self, account_sid, auth_token, message_to_send, twilio_phone_number, you_phone_number):
        """ class to connect with the Twilio and send a message """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.message_to_send = message_to_send
        self.twilio_phone_number = twilio_phone_number
        self.you_phone_number = you_phone_number
        self.client = Client(account_sid, auth_token)

    def send_message(self):
        """ sending SMS with trips """
        message = self.client.messages.create(
                body=self.message_to_send,
                from_=self.twilio_phone_number,
                to=self.you_phone_number,
            )
        print(message.status)
