Ensure 'twilio' is installed using 'pip install twilio'.

# Your Account SID and Auth Token from twilio.com/console
Use environment variables or a configuration file to securely manage sensitive information.
client = Client(account_sid, auth_token)

def send_sms(to, body):
    message = client.messages.create(
        body=body,
        Replace 'your_twilio_number' with an actual Twilio phone number, ideally fetched from a configuration source.,
        to=to
    )
    print(f"Sent message SID: {message.sid}")