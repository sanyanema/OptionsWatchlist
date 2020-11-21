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


# Returns the data that would be presented in table to the user
def findGreekData(optionChain):
    # Creates a dataframe with specific parameters from the entire option chain
    data = optionChain.loc[:, ('contractSymbol', 'strike', 'lastPrice', 'impliedVolatility')]
    additionalData = pd.DataFrame({"expirationDate": [],
                                   "typeOfOption": []})

    # Loops through every contract symbol and creates a row of data with the expiration date and option type
    for contract in optionChain['contractSymbol']:
        contract = parseContractSymbol(contract)
        new_row = {"expirationDate": findContractExpirationDate(contract), "typeOfOption": findContractType(contract)}
        # Appends the new row to a dataframe with the expiration dates and option types
        additionalData = additionalData.append(new_row, ignore_index=True)

    # Merges the new dataframe to the dataframe created with specific parameters
    data.loc[:, 'expirationDate'] = additionalData['expirationDate']
    data.loc[:, 'typeOfOption'] = additionalData['typeOfOption']
    return data


# Helper method to parses the contract symbol down to the form YYMMDD + option type
# def parseContractSymbol(contract):
#     index = 0
#     if (first_digit := re.search(r"\d", contract)) is not None:
#         contract = contract[first_digit.start()::]
#         try:
#             index = contract.index('C')
#         except ValueError:
#             index = contract.index('P')

#     contract = contract[0:index + 1]
#     return contract


# Helper method to get the contract type(Call/Put)
def findContractType(contract):
    if contract[len(contract) - 1] == 'C':
        return 'Call'
    else:
        return 'Put'


# Helper method to find the ticker name from a contract
# def findTickerName(contract):
#     if (first_digit := re.search(r"\d", contract)) is not None:
#         contract = contract[0:first_digit.start()]
#     return contract


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

# stock = getStock('TSLA')
# calls = getCalls('TSLA', '2020-11-20')
# print(calls)
# print()
# print()
# print(type(calls))
