import urllib.request
import re
from statistics import mean
import os

province = "quebec"
city = "laval"

def getGasPrices(province=province, city=city):
    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/'+ province +"/"+ city, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())
    lastIndexes, prices = [], []
    for match in re.finditer('StationDisplayPrice-module__price___3rARL">', html): 
        lastIndexes.append(match.end())
    for i in range (0, len(lastIndexes),1):
        index = int(lastIndexes[i]) + 1
        price = ""
        price += html[index] + html[index+1] + html[index+2] + html[index+3] + html[index+4]
        prices.append(float(price))
    return prices

def getStationAdresses(province=province, city=city):
    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/'+ province +"/"+ city, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())
    lastIndexOfAdress, listOfAdresses, listCitiesProvinces, finalList = [], [], [], []
    for match in re.finditer('<div class="StationDisplay-module__address___2_c7v">', html):
        lastIndexOfAdress.append(match.end())
    for i in range(0, len(lastIndexOfAdress) ,1):
        index, address = lastIndexOfAdress[i], ""
        while html[index] != '/':
            address+= html[index]
            index += 1
        address = address.replace("<br", "")
        listOfAdresses.append(address)
        city_province = ""
        index += 2
        while html[index] != '<':
            city_province += html[index]
            index += 1
        listCitiesProvinces.append(city_province)
    for i in range(0, len(listOfAdresses), 1): finalList.append(listOfAdresses[i] + " " + listCitiesProvinces[i])
    return finalList

def getGasStationNames(province=province, city=city):
    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/'+ province +"/"+ city, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())
    lastIndexOfAdress, gasStations = [], []
    for match in re.finditer('<h3 class="header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8">', html):
        lastIndexOfAdress.append(match.end())
    for x in range(0, len(lastIndexOfAdress),1):
        i, name = lastIndexOfAdress[x], ""
        while html[i].isupper() == False: i += 1
        while html[i] != "<":
            name += html[i]
            i+= 1
        gasStations.append(name)
    return gasStations

def lastUpdate(province=province, city=city):
    req = urllib.request.Request('https://www.gasbuddy.com/gasprices/'+ province +"/"+ city, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    html = str(urllib.request.urlopen(req).read())
    listUpdates, lastUpdates = [], []
    for match in re.finditer('<span class="ReportedBy-module__postedTime___J5H9Z">', html): listUpdates.append(match.end()) 
    for x in range(0, len(listUpdates), 1):
        i = listUpdates[x]
        update = ""
        while html[i] != "<":
            update += html[i]
            i +=1
        time = update.split(" ")
        hours = time[0]
        if int(hours) < 10: hours = "0" + hours
        time[0], newUpdate = hours, ""
        for z in range(0,len(time), 1): newUpdate += str(time[z]) + " "
        lastUpdates.append(newUpdate)
    
    return lastUpdates

def averageGasPrice(list_of_prices):
    average = str(round(mean(list_of_prices),1))
    average = average.replace(".","")
    average = average[:1] + "." + average[1:]
    return float(average)

def computeGasCost(kmStart, kmEnd, gasPrice):
    litresPerKm = 9.3/100    
    return round(((litresPerKm * (kmStart - kmEnd)) * gasPrice),2) 

# --- Main ---
os.system("cls")
print ("----- Gas App -----\n")
print ("1 - Trip Cost Calculator")
print (f"2 - View gas prices of default city ({city})")
print ("3 - View gas prices of another city")
print ("0 - Exit Program\n")
choice = input("--> ")
os.system("cls")

while choice != "0":
    
    if choice != "0":

        if choice == "1":
            
            kmStart = int(input("Enter the km at the start of the trip: "))
            kmEnd = int(input("Enter the km at the end of the trip: "))
            print (f"\nKm driven: {kmStart - kmEnd}\nTrip Cost: {computeGasCost(kmStart,kmEnd, averageGasPrice(getGasPrices()))} $\n")
            os.system("pause")
        
        elif choice == "2":
            
            station, price, last_update, address = "Station", "Price","Last Update", "Address"
            print (f"{station:<25}{price:^25}{last_update:^25}{address:<25}\n")
            for i in range(0, len(getGasPrices()), 1):
                price = str(getGasPrices()[i]) +" $/L"
                print(f"{getGasStationNames()[i]:<25}{price:^25}{lastUpdate()[i]:^25}{getStationAdresses()[i]:<25}")
            print("\n")
            os.system("pause")

        elif choice == "3":
            prov = input("Enter the province for the search: ")
            city = input("Enter the city for the search: ")
            
            os.system("cls")
            station, price, last_update, address = "Station", "Price","Last Update", "Address"
            print (f"{station:<25}{price:^25}{last_update:^25}{address:<25}\n")
            for i in range(0, len(getGasPrices(prov, city)), 1):
                price = str(getGasPrices()[i]) +" $/L"
                print(f"{getGasStationNames(prov, city)[i]:<25}{price:^25}{lastUpdate(prov, city)[i]:^25}{getStationAdresses(prov, city)[i]:<25}")
            print("\n")
            os.system("pause")
    


