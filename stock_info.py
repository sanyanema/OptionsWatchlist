""" This file shows examples of how to get data to display on the webpage"""

# import yfinance library
import yfinance as yf

tickerName = "GOOG"             # example ticker: GOOG
ticker = yf.Ticker(tickerName)  # create Ticker object
info = ticker.info              # get info


# RIGHT BANNER
# company name
name = info['longName']

# sector
sector = info['sector']

# current price
currentPrice = str(info['bid']) + " " + info['currency']

# day's range
dayRange = str(info['dayLow']) + " - " + str(info['dayHigh']) + " USD"

# 52 week range
yrRange = str(info['fiftyTwoWeekLow']) + " - " + str(info['fiftyTwoWeekHigh']) + " USD"

# average volume
avgVolume = str(info['averageVolume'])

# trailing EPS (uses historical data)
epsTrail = str(info['trailingEps'])

# forward EPS (uses forecasted data)
epsFwd = str(info['forwardEps'])

# market capital
marketCap = str(info['marketCap'])


# PRICE GRAPH
# get historical data. available periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. default = 1mo
historical = ticker.history(period='max')

# get closing prices from historical data
closePrice = historical.Close

def getTickerInfo(tickerName) :
    ticker = yf.Ticker(tickerName)  # create Ticker object
    return ticker.info

