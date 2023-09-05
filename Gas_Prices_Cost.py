import urllib.request
import re

def gasCosts(province, city):

    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/' + province + "/" + city, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())

    def replace_pattern(input_string, pattern, replacement):
        return re.sub(pattern, replacement, input_string)

    def getGasPrices(province=province, city=city):
        lastIndexes, prices = [], []
        for match in re.finditer('StationDisplayPrice-module__price___3rARL">', html):
            lastIndexes.append(match.end())

        for i in range(0, len(lastIndexes), 1):
            index = int(lastIndexes[i])
            count = 0
            price = ""

            while html[index] != '<':
                price += html[index]
                index += 1
            x = re.findall(r"[-+]?\d*\.\d+|\d+", price)
            rex = re.compile("^[0-9]{3}.[0-9]{1}$")
            for i in range(0, len(x), 1):
                if rex.match(x[i]): prices.append(float(x[i]))

        return prices


    def getStationAdresses(province=province, city=city):
        lastIndexOfAdress, listOfAdresses, listCitiesProvinces, finalList = [], [], [], []
        for match in re.finditer('<div class="StationDisplay-module__address___2_c7v">', html):
            lastIndexOfAdress.append(match.end())
        for i in range(0, len(lastIndexOfAdress), 1):
            index, address = lastIndexOfAdress[i], ""
            while html[index] != '/':
                address += html[index]
                index += 1
            address = address.replace("<br", "")
            address = replace_pattern(address, "\\\\xc3\\\\xa9", "e")
            listOfAdresses.append(address)
            city_province = ""
            index += 2
            while html[index] != '<':
                city_province += html[index]
                index += 1
            city_province = replace_pattern(city_province, "\\xc3\\xa9", "e")    
            listCitiesProvinces.append(city_province)
        for i in range(0, len(listOfAdresses), 1): finalList.append(listOfAdresses[i] + " " + listCitiesProvinces[i])
        return finalList


    def getGasStationNames(province=province, city=city):
        lastIndexOfAdress, gasStations = [], []
        for match in re.finditer(
                '<h3 class="header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8">',
                html):
            lastIndexOfAdress.append(match.end())
        for x in range(0, len(lastIndexOfAdress), 1):
            i, name = lastIndexOfAdress[x], ""
            while html[i].isupper() == False: i += 1
            while html[i] != "<":
                name += html[i]
                i += 1
            name = replace_pattern(name, "\\\\xc3\\\\xa9", "e")
            gasStations.append(name)
        return gasStations


    def lastUpdate(province=province, city=city):
        listUpdates, lastUpdates = [], []
        for match in re.finditer('<span class="ReportedBy-module__postedTime___J5H9Z">', html): listUpdates.append(
            match.end())
        for x in range(0, len(listUpdates), 1):
            i = listUpdates[x]
            update = ""
            while html[i] != "<":
                update += html[i]
                i += 1
            time = update.split(" ")
            hours = time[0]
            if int(hours) < 10: hours = "0" + hours
            time[0], newUpdate = hours, ""
            for z in range(0, len(time), 1): newUpdate += str(time[z]) + " "
            lastUpdates.append(newUpdate)

        return lastUpdates
    
    gasInfoList = []
    tempGasInfo = {}
    name, price, adress, update = "", "", "", ""
    for i in range(0, len(getGasPrices(province, city)), 1):
        name, price, adress, update = getGasStationNames(province, city)[i], getGasPrices(province, city)[i], getStationAdresses(province, city)[i], lastUpdate(province, city)[i]
        tempGasInfo = {
           "station_name": name,
            "price": price,
            "address": adress,
            "last_update": update
        }
        gasInfoList.append(tempGasInfo)
    return gasInfoList
