import yfinance as yf
import pandas as pd
import re


def getStock(ticker):
    return yf.Ticker(ticker)


def getExpirationDates(ticker):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    return expirations


def getCalls(ticker, date):
    return yf.Ticker(ticker).option_chain(date).calls


def getPuts(ticker, date):
    return yf.Ticker(ticker).option_chain(date).puts


def findRelevantData(optionChain):
    data = optionChain[['contractSymbol', 'strike', 'impliedVolatility', 'lastPrice']]
    additionalData = pd.DataFrame({"expirationDate": [],
                                   "typeOfOption": []})

    for contract in optionChain['contractSymbol']:
        expirationDate = '20'
        information = parseContractSymbol(str(contract))
        typeOfOption = information.charAt(len(information)-1)
        print(typeOfOption)
        for x in range(len(information)):
            if x<2:
                expirationDate = expirationDate


def parseContractSymbol(contract):
    if (first_digit := re.search(r"\d", contract)) is not None:
        contract = contract[first_digit.start()::]
    index = contract.index('C')
    contract = contract[0:index+1]
    return contract

print(getExpirationDates(getStock('BRK-B').ticker))

print(findRelevantData(getCalls('AAPL', '2020-10-09')))
