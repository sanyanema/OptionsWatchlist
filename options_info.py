import yfinance as yf
import pandas as pd
import re


# Returns Ticker object from Yahoo Finance when given a ticker
def getStock(ticker):
    return yf.Ticker(ticker)


# Returns all the possible expiration dates of a ticker
def getExpirationDates(ticker):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    return expirations


# Returns the call options at a certain expiration date and ticker
def getCalls(ticker, date):
    return yf.Ticker(ticker).option_chain(date).calls


# Returns the puts options at a certain expiration date and ticker
def getPuts(ticker, date):
    return yf.Ticker(ticker).option_chain(date).puts


# Returns the data that would be presented in a table to the user
def findRelevantData(optionChain):
    data = optionChain[['contractSymbol', 'strike', 'impliedVolatility', 'lastPrice']]
    additionalData = pd.DataFrame({"expirationDate": [],
                                   "typeOfOption": []})

    for contract in optionChain['contractSymbol']:
        expirationDate = '20'
        information = parseContractSymbol(str(contract))
        for x in range(len(information)):
            if x < 2:
                expirationDate = expirationDate


# Parses the contract symbol down to the form YYMMDD and option type
def parseContractSymbol(contract):
    if (first_digit := re.search(r"\d", contract)) is not None:
        contract = contract[first_digit.start()::]
    index = contract.index('C')
    contract = contract[0:index + 1]
    return contract


#Testing
print(getExpirationDates(getStock('BRK-B').ticker))

print(findRelevantData(getCalls('AAPL', '2020-10-09')))
