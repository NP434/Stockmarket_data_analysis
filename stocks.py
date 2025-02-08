"""
Author: Noah Perea with help from chat gpt
ChatGPT contributed to the sorting method of the original dictionary in download data, as well as compilling the data into
the close list, and finally with allowing the program to run from the command line.

Purpose: Practice pulling data from the web, sorting it, and obtaining speciifc values from it before storing those in a json file

"""

from urllib.request import urlopen
from requests import get
from datetime import date 
from json import dump
import sys

def download_data(ticker: str)-> dict:
    """This function downloads data from the nasdaq website, converts it to a json then sorts it based on date before creating a dictionary with keys being the dates"""
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = base_url + path #Combines the two parts of the URL together
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"} #Allows acces to the website
    try:
        """This section is is where the data is pulled and converted into a dictionary"""
        response = get((URL), headers=headers)
        raw_data = response.json() #Converts the data to json
        data = sorted(raw_data['data']["tradesTable"]["rows"], key = lambda x: x['date']) #This combs through and retrieves all the rows with actual stock data
        data_dict = {item["date"]: item for item in data} #This creates a dictionary with the keys being the dates of the reported stock prices.
        return data_dict
    except Exception as e:
        print(e)

def avg(lst: list)-> float:
    """A function to calculate the average of all values in a list"""
    lsum = 0 
    for i in lst:
        lsum += i # sums all values of the list hence name l(ist)sum
    fsum = lsum / len(lst) #the final sum is calculated by dividing the list sum by the number of items in the list
    return fsum

def median(lst:list)-> float:
    """A function to return the median value of the list"""
    ordered_lst = sorted(lst) # sorts the list
    med_item = int(len(lst) / 2) #finds the index of the middle item in the list
    med_val = ordered_lst[med_item] #gets the value of the middle item in the list
    return med_val

def data_processing(data_dict: dict, ticker: str) -> dict:
    """This function calculates all the max, min,median, and avg of the given stock data"""
    closing_data = [] # empty list to be added to
    for key, item in data_dict.items(): 
        """This section iterates through the intermediate dictionary to add all values of close and add them to a list"""
        closing_value = item.get("close") #Gets the value of the close for that entry
        removed_str = closing_value.replace("$","").strip() #Removes the dollar sign from that entry
        closing_data.append(float(removed_str)) #Converts the value to a float so that it can be used for calculations
    max_close = max(closing_data) 
    min_close = min(closing_data)
    avg_close = avg(closing_data)
    median_close = median(closing_data)
    Output_dict = {"Min: ": min_close, "Max: ": max_close, "Avg: ": avg_close, "Median: ": median_close, "Ticker: ": ticker}
    return Output_dict

def data_package(ticker: str)->dict:
    """This is a helper function that calls the download data and data processing functions, and returns the fully"""
    intermediate_data = download_data(ticker) 
    end_dict = data_processing(intermediate_data,ticker)
    return end_dict



if __name__ == "__main__":
    """This allows for the program to be called from the python command line"""
    i = 1 
    if len(sys.argv) > 1: #checks if there are arguments when the program is called from the command line
        with open("Stocks.json", "w") as file: #opens the stocks.json file
            while i < len(sys.argv): #if there are multiple args, increments through them
                ticker = sys.argv[i] # gets the inputed ticker arg
                final_dict = data_package(ticker)
                dump(final_dict, file) # places the data into the json file
                file.write("\n") #adds a new line after each data entry
                i += 1 #increments the loop varaible
       
