"""
Author: Noah Perea with help from chat gpt

"""

from urllib.request import urlopen
from requests import get
from datetime import date 
from json import dump
import sys

def download_data(ticker: str)-> dict:
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = base_url + path
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    try:
        response = get((URL), headers=headers)
        raw_data = response.json()
        data = sorted(raw_data['data']["tradesTable"]["rows"], key = lambda x: x['date'])
        data_dict = {item["date"]: item for item in data}
        return data_dict
    except Exception as e:
        print(e)

def avg(lst: list)-> float:
    lsum = 0
    for i in lst:
        lsum += i
    fsum = lsum / len(lst)
    return fsum

def median(lst:list)-> float:
    ordered_lst = sorted(lst)
    med_item = int(len(lst) / 2)
    med_val = ordered_lst[med_item]
    return med_val

def data_processing(data_dict: dict, ticker: str) -> dict:
    closing_data = []
    for key, item in data_dict.items():
        closing_value = item.get("close")
        removed_str = closing_value.replace("$","").strip()
        closing_data.append(float(removed_str))
    max_close = max(closing_data)
    min_close = min(closing_data)
    avg_close = avg(closing_data)
    median_close = median(closing_data)
    Output_dict = {"Min: ": min_close, "Max: ": max_close, "Avg: ": avg_close, "Median: ": median_close, "Ticker: ": ticker}
    return Output_dict

def data_package(ticker: str)->dict:
    intermediate_data = download_data(ticker)
    end_dict = data_processing(intermediate_data,ticker)
    return end_dict



if __name__ == "__main__":
    i = 1
    if len(sys.argv) > 1:
        with open("Stock.json", "w") as file:
            while i < len(sys.argv):
                ticker = sys.argv[i]
                final_dict = data_package(ticker)
                dump(final_dict, file)
                file.write("\n")
                i += 1
       
