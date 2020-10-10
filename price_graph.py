import matplotlib.pyplot as plt
import yfinance as yf
import json


class PriceGraph:
    # this class represents a price graph object for a given stock ticker
    # creating an instance of PriceGraph creates an object containing the name of the ticker and empty data list
    # if getPriceHistory is called, it sets the value of data to a dataframe containing the closing price history
    # if plotPriceHistory is called, it gets the price history AND plots it for max period

    def __init__(self, tickerName):
        self.data = []
        self.ticker = tickerName

    def getPriceHistory(self):
        stock = yf.Ticker(self.ticker)

        # check if empty
        if stock.history(period='max').empty:
            raise NameError("Not a valid symbol")
        else:
            self.data = stock.history(period='max')

    def plotPriceHistory(self):
        self.getPriceHistory()
        self.data.plot(y='Close')
        plt.title(self.ticker)
        plt.legend().remove()
        plt.ylabel('Closing Price (USD)')
        plt.show()


# creating a PriceGraph object and plotting its price history
google = PriceGraph('GOOG')
google.plotPriceHistory()
