""" This file defines the class StockInfo.

    A new instance of StockInfo contains the necessary info about the stock to be
    displayed on the visualization page.

    The instance method getHist returns the close price history for the desired period.
 """

# import yfinance library
import yfinance as yf


class StockInfo:
    def __init__(self, tickerName):
        """
        class creates object containing relevant info for desired stock
        :param tickerName: [string] stock ticker
        """
        # create Ticker object
        self.ticker = yf.Ticker(tickerName)

        # get info
        info = self.ticker.info

        # company name
        self.name = info['longName']

        # sector
        self.sector = info['sector']

        # current price
        self.current_price = str(info['bid']) + " " + info['currency']

        # day's range
        self.day_range = str(info['dayLow']) + " - " + str(info['dayHigh']) + " USD"

        # 52 week range
        self.yr_range = str(info['fiftyTwoWeekLow']) + " - " + str(info['fiftyTwoWeekHigh']) + " USD"

        # average volume
        self.avg_volume = str(info['averageVolume'])

        # trailing EPS (uses historical data)
        self.eps_trail = str(info['trailingEps'])

        # forward EPS (uses forecasted data)
        self.eps_fwd = str(info['forwardEps'])

        # market capital
        self.market_cap = str(info['marketCap'])

    def get_hist(self, period):
        """ function retrieves close price history for desired stock

        :param period: [string] desired graphing period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
        :return: [pandas dataframe] dataframe of historical closing prices
        """

        # check if period is valid
        periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if period not in periods:
            invalid_period_msg = "getHist: period must be one of: " + ', '.join(periods)
            raise ValueError(invalid_period_msg)

        # get historical data. available periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. default = 1mo
        historical = self.ticker.history(period=period)

        # get closing prices from historical data
        close_price = historical.Close

        return close_price


# example code
google = StockInfo("goog")
print(google.sector)
print(google.get_hist("5mo"))
