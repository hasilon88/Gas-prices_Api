from flask import Flask
from flask_cors import CORS, cross_origin
import urllib.request
import re

def getGasPrices(html):
    regex = re.compile(r'StationDisplayPrice-module__price___3rARL">')
    matches = [match.end() for match in regex.finditer(html)]
    prices = []

    for index in matches:
        price_text = ""
        while html[index] != '<':
            price_text += html[index]
            index += 1
        price_parts = re.findall(r"[-+]?\d*\.\d+|\d+", price_text)
        rex = re.compile("^[0-9]{3}.[0-9]{1}$")
        valid_prices = [float(x) for x in price_parts if rex.match(x)]
        prices.extend(valid_prices)

    return prices

def getStationAddresses(html):
    regex = re.compile(r'<div class="StationDisplay-module__address___2_c7v">')
    matches = [match.end() for match in regex.finditer(html)]
    addresses = []

    for index in matches:
        address_text = ""
        while html[index] != '/':
            address_text += html[index]
            index += 1
        address_text = address_text.replace("<br", "").replace("\\xc3\\xa9", "e")
        addresses.append(address_text)

    return addresses

def getGasStationNames(html):
    regex = re.compile(r'<h3 class="header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8">')
    matches = [match.end() for match in regex.finditer(html)]
    gas_stations = []

    for index in matches:
        i = index
        name_text = ""
        while html[i].isupper() is False:
            i += 1
        while html[i] != "<":
            name_text += html[i]
            i += 1
        name_text = name_text.replace("\\\\xc3\\\\xa9", "e")
        gas_stations.append(name_text)

    return gas_stations

def lastUpdate(html):
    regex = re.compile(r'<span class="ReportedBy-module__postedTime___J5H9Z">')
    matches = [match.end() for match in regex.finditer(html)]
    last_updates = []

    for index in matches:
        i = index
        update_text = ""
        while html[i] != "<":
            update_text += html[i]
            i += 1
        time_parts = update_text.split()
        if len(time_parts) >= 2:
            hours = int(time_parts[0])
            if hours < 10:
                time_parts[0] = "0" + time_parts[0]
            new_update = " ".join(time_parts[:2])
            last_updates.append(new_update)

    return last_updates

def get_gas_info(province, city):
    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/' + province + "/" + city, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())
    
    gas_prices = getGasPrices(html)
    station_addresses = getStationAddresses(html)
    gas_station_names = getGasStationNames(html)
    last_updates = lastUpdate(html)

    min_length = min(len(gas_prices), len(station_addresses), len(gas_station_names), len(last_updates))

    gas_info_list = [
        {
            "station_name": gas_station_names[i],
            "price": gas_prices[i],
            "address": station_addresses[i],
            "last_update": last_updates[i]
        }
        for i in range(min_length)
    ]

    return gas_info_list

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def landingPage():
  return """
            Hello, to get gas prices and other info, please add the province and the city in the URL <br/>
            For example: /ontario/toronto
        """

@cross_origin()
@app.get('/<province>/<city>')
def get_info(province, city):
    return get_gas_info(str(province).lower(), str(city).lower())
 
 
# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server
    app.run(debug=True)