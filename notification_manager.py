from twilio.rest import Client
from data_manager import DataManager
import smtplib

# https://www.twilio.com/
MY_TWILIO_ACCOUNT_SID = "your_twilio_sid"
MY_TWILIO_ACCOUNT_TOKEN = "your_twilio_token"
MY_TWILIO_PHONE_NUMBER = "your_twilio_number"
MY_PERSONAL_PHONE_NUMBER = "your_private_number"
MY_EMAIL_ADDRESS = "your_private_email_for_testing"
MY_EMAIL_PASSWORD = "your_email_password"


class NotificationManager:
    def __init__(self):
        self.account_sid = MY_TWILIO_ACCOUNT_SID
        self.auth_token = MY_TWILIO_ACCOUNT_TOKEN
        self.email_sheet = DataManager()
    # comparing the best online prices with price that I am willing to pay for a flight according to my sheety sheet
    def compare_prices(self, sheet, online):
        sheet_prices = sheet
        online_prices = online
        links = ""
        for i in range(0, len(sheet_prices)):
            if online_prices[i][0] == "NO":
                continue
            # if the online price is lower then price in my sheety sheet then an SMS will be sent with flight details
            elif online_prices[i][1] <= sheet_prices[i]:
                client = Client(self.account_sid, self.auth_token)
                message = client.messages.create(
                    body=online_prices[i][0],
                    from_=MY_TWILIO_PHONE_NUMBER,
                    to=MY_PERSONAL_PHONE_NUMBER
                )
                links += f"{online_prices[i][0]} \n{online_prices[i][2]} \n"
                print(message.status)
                print("LOW")
            else:
                print("Too expensive")

        emails = self.email_sheet.get_emails()
        my_email = MY_EMAIL_ADDRESS
        my_pass = MY_EMAIL_PASSWORD
        # if the online price is lower then price in my sheety sheet then an email will be sent with flight details
        # and booking link to people from my users sheety sheet
        for user in emails['users']:
            email = user['emailAddress']

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_pass)
                connection.sendmail(from_addr=my_email, to_addrs=email,
                                    msg=f"Subject: Low Price Alert!!!\n\n Follow links below for cheap flight tickets:\n{links}")

