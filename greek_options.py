from wallstreet import Stock, Call, Put
import yfinance

# Wallstreet library can scrap google finance or yahoo
# Make sure to set source to yahoo for continuity with yfinance library
apple = Stock('AAPL', source='yahoo')
applecall = Call('AAPL', d=30, m=10, y=2020, strike=130, source='yahoo')

# All the greek options can be called easily with this
print(applecall.delta())
print(applecall.theta())
print(applecall.gamma())
print(applecall.rho())
print(applecall.vega())

# TODO method creating yfinance ticker object and extracting data to feed into Wallstreet for greeks


# TODO method converting a YYYY-MM-DD string to separate variables for year, month, and day


# TODO method to get greeks given a option contract symbol
