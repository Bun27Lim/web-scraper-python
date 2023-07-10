# Yahoo Stock Webscraper

## Description
Using python, this is a practice project for webscraping.
This application scrapes the most active stock tab from Yahoo Finance
The stock data is exported to a csv and xlsx file for further analysis and manipulation.

## How it Works
1. Make an http request to the yahoo
2. Parse HTML code using Beautiful soup
3. Locate the information on the webpage using find function from Beautiful soup
4. Going through each stock one by one puts the data in a dictionary
5. Dictionary is added to the list of all the stock data
6. Using stocklist output data to csv and excel using csv and pandas respectively

##Packages and Modules used
1. requests: for communicated with http
2. bs4:for parsing html code
3. csv:for csv output
4. pandas: for readable outputs
5. openpyxl: for excel

Resources used:
Yahoo Finance
