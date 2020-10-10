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


# Returns the data that would be presented in the table to the user
def findRelevantData(optionChain):
    data = optionChain.loc[:, ('contractSymbol', 'strike', 'lastPrice', 'impliedVolatility')]
    additionalData = pd.DataFrame({"expirationDate":[],
                                   "typeOfOption":[]})

    for contract in optionChain['contractSymbol']:
        contract = parseContractSymbol(contract)
        new_row = {"expirationDate": findContractExpirationDate(contract), "typeOfOption": findContractType(contract)}
        additionalData = additionalData.append(new_row, ignore_index=True)
        data.loc[:, 'expirationDate'] = additionalData['expirationDate']
        data.loc[:, 'typeOfOption'] = additionalData['typeOfOption']
    return data


# Helper method to parses the contract symbol down to the form YYMMDD + option type
def parseContractSymbol(contract):
    if (first_digit := re.search(r"\d", contract)) is not None:
        contract = contract[first_digit.start()::]
    index = contract.index('C')
    contract = contract[0:index + 1]
    return contract


# Helper method to get the contract type(Call/Put)
def findContractType(contract):
    if contract[len(contract) - 1] == 'C':
        return 'Call'
    else:
        return 'Put'


# Helper method to get the expiration date in the form YYYY-MM-DD
def findContractExpirationDate(contract):
    expirationDate = '20'
    counter = 0
    for character in contract:
        if counter < 6:
            if counter % 2 == 0 and counter > 0:
                expirationDate = expirationDate + "-"
            expirationDate = expirationDate + character
        counter += 1
    return expirationDate


# Testing

print(findRelevantData(getCalls('AAPL', '2020-10-16')))

