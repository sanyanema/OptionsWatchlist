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
    info = [i.split("(")[1] for i in info] # getting only the change from all of the info
    info = [i.split(")")[0] for i in info]
    watchlist_dict = {getTicker(name[i]): {'change' : {'percent' : info[i], 'color' : getColor(info[i])}, 'name' : name[i], 'price' : price[i]} for i in range(len(info))}
    return watchlist_dict

def getTicker(name):
    start = name.index('(')
    end = name.index(')')
    return name[start + 1 : end]
        
def getColor(num):
    if '-' in num:
        return "red"
    elif "+" in num:
        return "green"
