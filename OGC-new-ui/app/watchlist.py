#from .models import Transaction, Account

#https://finance.yahoo.com/quote/aapl

#instead of aapl do 

import requests
from bs4 import BeautifulSoup


def getWatchListInfo(watchlist):
    info = dict()
    name = []
    change = []
    for stock in watchlist:
        if stock is not None:
            url = "https://finance.yahoo.com/" + stock
            result = requests.get(url)
            source = result.content
            soup = BeautifulSoup(source, 'lxml')
            stockname = soup.find('div', {'data-reactid': '28'}).find('td', {'class': "data-col1 Ta(start) Pstart(10px) Miw(180px)"})

watchlist = ["aapl", "zm"]
print(getWatchListInfo(watchlist))

