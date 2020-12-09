import urllib3
from bs4 import BeautifulSoup
import re
from collections import namedtuple


def getTrendingTickers():
    req = urllib3.PoolManager()
    res = req.request('GET', "https://finance.yahoo.com/trending-tickers")

    soup = BeautifulSoup(res.data, 'html.parser')

    req = urllib3.PoolManager()
    res = req.request('GET', "https://finance.yahoo.com/trending-tickers")

    soup = BeautifulSoup(res.data, 'html.parser')

    names = soup.find('tbody', {'class': ''}).findAll('td', {'class': "data-col1 Ta(start) Pstart(10px) Miw(180px)"})
    companies = []
    for name in names:
        name = name.get_text()
        companies.append(name)
    
    change = soup.find('tbody', {'class': ''}).findAll('td', {'class': "data-col5 Ta(end) Pstart(20px)"})
    amounts = []
    for percent in change:
        percent = percent.get_text()
        amounts.append(percent)
    
    trending = {companies[i] : amounts[i] for i in range(len(amounts))}   
    return AddColor(trending)


def getColor(num):
    if '-' in num:
        return "red"
    elif "+" in num:
        return "green"

def AddColor(ticker_values):
    # remove + and % for easy float conversion
    tickers_full = dict()
    # format of each element
    # Apple : (-0.9, red)
    for key in ticker_values.keys():
        tickers_full[key] = {'change': ticker_values[key],
                             'color': getColor(ticker_values[key])}
    return tickers_full



def getBiggestGainers():
    req = urllib3.PoolManager()
    res = req.request('GET', "https://finance.yahoo.com/gainers")

    soup = BeautifulSoup(res.data, 'html.parser')

    names = soup.find('tbody', {'class': ''}).findAll('td', {'class': "Va(m) Ta(start) Px(10px) Fz(s)"})

    change = soup.find('tbody', {'class': ''}).findAll('td', {'class': "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"})

    companies = []
    amounts = []
    gainers = dict()

    for company in names:
        company = str(company)
        first_index = company.find("-->")
        second_index = company.find(" /react-text")
        company = company[first_index + 3:second_index - 4]
        companies.append(company)
    for amount in change:
        amount = str(amount)
        if '%' in amount:
            amount = amount.replace(
                'aria-label="% Change" class="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)" colspan="" data-reactid=', '')
            amount = amount.replace('><span class="Trsdu(0.3s) Fw(600) C($positiveColor)" data-reactid=', '')
            first_index = amount.find('>')
            second_index = amount.find('</')
            amount = amount[first_index + 1:second_index]
            amounts.append(amount)

    if len(companies) == len(amounts):
        for x in range(0, len(companies)):
            gainers[companies[x]] = amounts[x]

    return gainers


def getBiggestLosers():
    req = urllib3.PoolManager()

    res = req.request('GET', "https://finance.yahoo.com/losers")

    soup = BeautifulSoup(res.data, 'html.parser')

    names = soup.find('tbody', {'class': ''}).findAll('td', {'class': "Va(m) Ta(start) Px(10px) Fz(s)"})

    change = soup.find('tbody', {'class': ''}).findAll('td', {'class': "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"})

    companies = []
    amounts = []
    losers = dict()

    for company in names:
        company = str(company)
        first_index = company.find("-->")
        second_index = company.find(" /react-text")
        company = company[first_index + 3:second_index - 4]
        companies.append(company)
    for amount in change:
        amount = str(amount)
        if '%' in amount:
            amount = amount.replace(
                'aria-label="% Change" class="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)" colspan="" data-reactid=', '')
            amount = amount.replace('><span class="Trsdu(0.3s) Fw(600) C($negativeColor)" data-reactid=', '')
            first_index = amount.find('>')
            second_index = amount.find('</')
            amount = amount[first_index + 1:second_index]
            amounts.append(amount)

    if len(companies) == len(amounts):
        for x in range(0, len(companies)):
            losers[companies[x]] = amounts[x]

    return losers

