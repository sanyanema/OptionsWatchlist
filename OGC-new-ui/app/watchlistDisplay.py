#from .models import Transaction, Account

#https://finance.yahoo.com/quote/aapl

#instead of aapl do 

import requests
from bs4 import BeautifulSoup


def getWatchListInfo(watchlist):
    temp = dict()
    name = []
    change = []
    price = []
    info = []
    if (len(watchlist) == 0): # accounts for if the watchlist is empty 
        return temp
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
    #print(info[0].split(")")[1]) # time the stock was updated
    #time = [info[0].split(")")[1]]
    # for i in range(len(info)):
    #     time.append(info[i].split(")")[1])
    # print(time)
    info = [i.split("(")[1] for i in info] # getting only the change from all of the info
    info = [i.split(")")[0] for i in info]
    watchlist_dict = {name[i]: {'change' : {'percent' : info[i], 'color' : getColor(info[i])}, 'price' : price[i]} for i in range(len(info))} # creating dict to map from name to change 
    
    return watchlist_dict
            
def getColor(num):
    if '-' in num:
        return "red"
    elif "+" in num:
        return "green"

