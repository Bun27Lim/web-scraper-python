import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


#Web scraper to scrape information from active stocks
url ="https://finance.yahoo.com/most-active"
csv_file_name = "stock_data.csv"
excel_file_name = "stock_data.xlsx"

#stockinterest = ['AMD', 'TSLA', 'NVDA']

response = requests.get(url)  #Using the requests library to retrieve the HTML code from URL store it in a response variable

soup = BeautifulSoup(response.text, "html.parser") #Variable to hold the parsed HTML

#List of dictionary to hold all stock the stock data
stockdata = []

#Output Labels
headernames = ['Symbol', 'Name', 'Price', '% Change', 'Volume', 'Market Cap']

#Function that orders the stock data from highest percent change
#Highest percent change includes negative and positive change
def orderByChange(list):
    return sorted(list, key=lambda x: abs(x['% Change']), reverse=True)


def orderByPrice(list):
    return sorted(list, key=lambda x: x['Price'], reverse=True)

#Key function for the parameter of sorted to sort the numbers with M representing millions and B representing Billions
#Volume usually never reaches to billions*******
def keyVolumeSort(num):

    #Get the value of volume using the dictionary key
    volume = num['Volume']

    multiplier = 1 # Default Multiplier
    if volume[-1] == 'M':
        multiplier = 2 # Arbitrary number to multiply number that is indicated in Millions
        volume = volume[:-1] # Removes M in the volume to multiply
    elif volume[-1] == 'B':
        multiplier = 3 # Arbitrary number to multiply number that is indicated in Billions
        volume = volume[:-1] # Removes B in the volume to multiply
    
    return float(volume) * multiplier
        
# Order by volume from highest to lowest
def orderByVolume(list):
    return sorted(list, key=keyVolumeSort, reverse=True)

#Function to create a csv file to write the data to
with open("stock_data.csv", 'w', newline='') as csv_file:
    
    #Get table to navigate
    #Using the inspect tool on the webpage tbody contains all the necessary information
    table_rows = soup.find("tbody").find_all('tr', {'class': 'simpTblRow'})

    for row in table_rows:

        #Create a new dictionary for each instance since dictionary are mutable objects
        stock = {
            'Symbol': "",
            'Name'  : "",
            'Price' : "",
            '% Change': "",
            'Volume': "",
            'Market Cap': "",
        }

        #Add data to the corresponding attributes
        stock['Symbol'] = row.find('a').text
        stock['Name'] = row.find('td', {'aria-label': 'Name'}).text
        stock['Price'] = float(row.find('td', {'aria-label': 'Price (Intraday)'}).text)             #Change to float for sorting purposes
        stock['Volume'] = row.find('td', {'aria-label': 'Volume'}).text                             
        stock['% Change'] = float(row.find('td', {'aria-label': '% Change'}).text.rstrip('%'))      #Change to float for sorting purposes
        stock['Market Cap'] = row.find('td', {'aria-label': 'Market Cap'}).text       
        #Add current stock to the list
        stockdata.append(stock)

    ## Can use excel to sort the data instead
    ## Sorting functions are functional and added for future purposes

    #stockdata = orderByChange(stockdata)

    #stockdata = orderByVolume(stockdata)

    #stockdata = orderByPrice(stockdata)

    #Write to csv file
    csv_writer = csv.DictWriter(csv_file, fieldnames=headernames)
    csv_writer.writeheader()
    csv_writer.writerows(stockdata)

    #Write to Excel File
    dataframe = pd.DataFrame(stockdata)
    dataframe.to_excel(excel_file_name, index=True)
