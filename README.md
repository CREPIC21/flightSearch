# flightSearch
- create sheety sheet with your cities that you wish to visit
- create sheety sheet with users emails to send emails with booking link
- create twilio account for sending SMS
- create tequila.kiwi account for api requests regarding flights

When code is run it will:
- get list of cities from your sheet
- get IATA codes for each city in your sheet using tequila.kiwi api request
- update your sheet with recieved IATA codes
- search the best online flight price for next 6 monts(can be modified) for cities in your sheet using IATA codes
- compare best online price for each city with price that you are willing to pay from your sheet
- if online price matches price that you are willing to pay or it is lower than that it will send SMS to your phone with basic flight details and email with booking link
