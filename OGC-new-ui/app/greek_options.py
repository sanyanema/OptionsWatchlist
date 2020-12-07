import yfinance
from wallstreet import Call, Put
from . import options_info as op # Use this line when running the file through views.py
# import options_info as op # Use this line when trying to run this file directly

# WallStreet library can scrap google finance or yahoo
# Make sure to set source to yahoo for continuity with YFinance library

# Helper method converting a YYYY-MM-DD string to separate variables for year, month, and day
def dateConverter(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return [year, month, day]


# Method inputting relevant data and strike price to extract data to feed into WallStreet for greeks
def yFinanceToWallStreet(optionChain, strikePrice):
    # Gets the relevant data to calculate greeks
    data = op.findGreekData(optionChain)
    # Gets the specific row with strike price wanted
    optionContract = data.loc[data['strike'] == strikePrice]

    # Checks if the option contract is a call
    if optionContract.iloc[0]['typeOfOption'] == 'Call':
        # Gets the date and converts it to work with WallStreet
        date = dateConverter(optionContract.iloc[0]['expirationDate'])
        # Returns the Call object that will be used to find greeks
        return Call(
            op.findTickerName(optionContract.iloc[0]['contractSymbol']),
            d=date[2], m=date[1], y=date[0],
            strike=strikePrice, source='yahoo')
    # If not a call option, assumes it is a Put option
    else:
        # Gets the date and converts it to work with WallStreet
        date = dateConverter(optionContract.iloc[0]['expirationDate'])
        # Returns the Put object that will be used to find greeks
        return Put(
            op.findTickerName(optionContract.iloc[0]['contractSymbol']),
            d=date[2], m=date[1], y=date[0],
            strike=strikePrice, source='yahoo')


# Method to get greeks given a option object from WallStreet
def getGreeks(option):
    # greeks = {"delta": option.delta(), "gamma": option.gamma(), "rho": option.rho(),
    #           "vega": option.vega(), "theta": option.theta()}
    greeks = (option.delta(), option.gamma(), option.rho(), option.vega(), option.theta())
    return greeks


# Testing
# print(getGreeks(yFinanceToWallStreet(yfinance.Ticker('TSLA').option_chain("2020-11-20").calls, 500)))
