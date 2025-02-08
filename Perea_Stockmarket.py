"""
Author: Noah Perea with help from chat gpt

"""

from urllib.request import urlopen
from requests import get
from datetime import date 
from json import loads,load

def download_data(ticker: str)-> dict:
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = base_url + path
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = get((URL), headers=headers)
    raw_data = response.json()
    data = sorted(raw_data['data']["tradesTable"]["rows"], key = lambda x: x['date'])
    data_dict = {item["date"]: item for item in data}
    return data_dict

    



print(download_data("AAPL"))