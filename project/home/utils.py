# utils.py
from twilio.rest import Client
from django.conf import settings

def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            to=phone_number, 
            from_="+1 689 215 8629",
            body=message)
        return True, message.sid
    except Exception as e:
        return False, str(e)
