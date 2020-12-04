#from .models import Transaction, Account

#https://finance.yahoo.com/quote/aapl

#instead of aapl do 

import requests
from bs4 import BeautifulSoup


def getWatchListInfo(watchlist):
    #info = dict()
    name = []
    change = []
    price = []
    info = []
    for stock in watchlist:
        if stock is not None:
            url = "https://finance.yahoo.com/quote/" + stock
            result = requests.get(url)
            source = result.content
            soup = BeautifulSoup(source, 'html.parser')
            stockname = soup.find('h1') # retrieves name of stock
            if stockname is not None:
                stockname = stockname.get_text()
            name.append(stockname)
            priceOf = soup.find('div', {'class' : 'D(ib) Mend(20px)'}) # retrieves price of stock
            if priceOf is not None:
                priceOf = priceOf.find('span').get_text()
                price.append(priceOf)
            total_info = soup.find('div', {'class' : 'D(ib) Mend(20px)'})
            if total_info is not None:
                total_info = total_info.get_text()
                info.append(total_info)
    info = [i.split("(")[1] for i in info] # getting only the change from all of the info
    info = [i.split(")")[0] for i in info]
    watchlist_dict = {name[i]: {'change' : {'percent' : info[i], 'color' : getColor(info[i])}, 'price' : price[i]} for i in range(len(info))} # creating dict to map from name to change 
    
    return watchlist_dict
            
def getColor(num):
    if '-' in num:
        return "red"
    elif "+" in num:
        return "green"

def AddColor(watchlist):
    # remove + and % for easy float conversion
    colored_watchlist = dict()
    # format of each element
    # Apple : (-0.9, red)
    # for key, value in watchlist.items():
    #     #print(value['change'])
    #     for key1, value1 in value.items():
    #         colored_watchlist[key1] = {'color' : getColor(value1),
    #                                     'percent' : value[key1]}
    for key, value in watchlist.items():
        # value contains the dict of change and price
        # want to change key == 'change' with change and color
        for key1, value1 in value.items():
            value['change'] = {'color' : getColor(value['change'])}
    return colored_watchlist
            
#
# watchlist = ["aapl", "zm", 'googl']
# print(getWatchListInfo(watchlist))

