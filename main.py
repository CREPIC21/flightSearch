from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

new_sheet = DataManager()
notification = NotificationManager()

# getting the whole sheet data
data = new_sheet.get_sheety_data()
# getting all columns from the sheet
data = data['prices']
# getting prices from column "Lowest Price" from the sheet
price = [item['lowestPrice'] for item in data]
# getting each city name with their sheet id from the sheet
cities = [{'city': item['city'], 'id': item['id']} for item in data ]


# creating a FlightSearch object from cities array
flight_search = FlightSearch(cities)
# getting IATA code for each city in the cities array
response = flight_search.saerching_iata_codes()
# updating my sheety sheet with IATA codes
codes = new_sheet.update_sheety_data(response)
# getting online prices for each city in cities array
online_prices = flight_search.check_flights(codes)
# comparing online prices with maximum prices in my sheety sheet that I am willing to pay for a trip
notification.compare_prices(price, online_prices)





