import requests
from pprint import pprint
import datetime


API_KIWI = "your_kiwi_apikey"   #https://tequila.kiwi.com/portal/login
MIN_PRICE = 570

class FlightSearch:
    def __init__(self, cities):
        # list of cities from my sheety sheet
        self.city_name = cities
        # departure city by your choice
        self.city_departure = "LON"
        # URL to make search queries
        self.location = "https://tequila-api.kiwi.com/locations/query"
        self.custom_header = {
            "apikey": API_KIWI,
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json"
        }
        # getting today's date from which to start search flights
        self.date = datetime.datetime.now().date().strftime("%d/%m/%Y")
        # getting date six months from today until which to search for flights
        self.date_six_months_from_today = (datetime.datetime.now() + datetime.timedelta(days=180)).strftime("%d/%m/%Y")

    # getting IATA codes for each city in my sheety sheet
    def saerching_iata_codes(self):
        codes = []

        for city in self.city_name:
            param = {
                "term": city['city']
            }
            response = requests.get(url=self.location, params=param, headers=self.custom_header)
            response.raise_for_status()
            data_loc = response.json()
            if len(data_loc['locations'][0]['code']) != 3:
                code_airport = data_loc['locations'][1]['code']
            else:
                code_airport = data_loc['locations'][0]['code']
            code = (city['id'], code_airport)
            codes.append(code)
        # print(f"TESTING {self.city_name}")
        return codes
        print(self.city_name)

    # searching for available flights to my desirable destinations in cities array getting the best online prices for
    # each city in cities array
    def check_flights(self, codes):
        location = "https://tequila-api.kiwi.com/v2/search"
        prices_array = []
        for code in codes:
            is_flight = True
            stopovers = 0
            while is_flight:
                param = {
                    "fly_from": self.city_departure,
                    "fly_to": code,
                    "date_from": self.date,
                    "date_to": self.date_six_months_from_today,
                    "flight_type": "round",
                    "nights_in_dst_from": 7,
                    "nights_in_dst_to": 28,
                    "curr": "GBP",
                    "max_sector_stopovers": stopovers,
                }
                # making api request with parameters above to search for flight
                response = requests.get(url=location, params=param, headers=self.custom_header)
                response.raise_for_status()
                data_loc = response.json()
                min_price = MIN_PRICE
                for item in data_loc['data']:
                    # pprint(item)
                    if item['conversion']['GBP'] < min_price:
                        min_price = item['conversion']['GBP']
                        dep_city = item['cityFrom']
                        dep_code = item['routes'][0][0]
                        arr_city = item['cityTo']
                        arr_code = item['routes'][0][1]
                        out_date = item['route'][0]['local_departure'].split("T")[0]
                        if item['route'][0]['flyTo'] != arr_code:
                            stopover = item['route'][0]['cityTo']
                            in_date = item['route'][3]['local_arrival'].split("T")[0]
                        else:
                            stopover = ""
                            in_date = item['route'][1]['local_arrival'].split("T")[0]
                        is_flight = False
                if not is_flight and min_price < MIN_PRICE:
                    # creating a message that will be sent via SMS
                    msg = f"{dep_city}-{dep_code} to {arr_city}-{arr_code} for {min_price}GBP\n{out_date}-{in_date}"
                    # creating a link for booking that will be sent via email
                    link = f"https://www.google.co.uk/flights?hl=en#flt={dep_code}.{arr_code}.{out_date}*{arr_code}.{dep_code}.{in_date}"
                    # checking if there is stopovers
                    if stopover:
                        msg += f"\nThere is one stopover in {stopover}."
                    msg_price = (msg, min_price, link)
                    prices_array.append(msg_price)
                else:
                    stopovers += 1
                if stopovers > 1:
                    is_flight = False
                    msg = "NO"
                    link = "NO"
                    msg_price = (msg, min_price, link)
                    prices_array.append(msg_price)
        pprint(prices_array)
        #print(msg)
        return prices_array

