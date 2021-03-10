import requests

MY_NAME = "your_sheety_name"
MY_EMAIL = "your_sheety_email"

class DataManager:
    def __init__(self):
        self.api_url = "your_sheety_prices_sheet_url"  #https://dashboard.sheety.co/login
    # getting data from my sheety sheet
    def get_sheety_data(self):
        response = requests.get(url=self.api_url)
        response.raise_for_status()
        data = response.json()
        return data
    # updating my sheety sheet with IATA codes
    def update_sheety_data(self, cities):
        codes = []
        for city in cities:
            codes.append(city[1])
            api_url = f"{self.api_url}{city[0]}"
            body = {
                "price": {
                    "name": MY_NAME,
                    "email": MY_EMAIL,
                    "iataCode": city[1],
                }
            }
            response = requests.put(url=api_url, json=body)
            response.raise_for_status()
        print(codes)
        return codes
    # getting customer emails from my users sheety sheet
    def get_emails(self):
        my_url = "your_sheety_users_sheet_url"

        response = requests.get(url=my_url)
        response.raise_for_status()
        data = response.json()
        return data
