""" This file defines the class StockInfo.

    A new instance of StockInfo contains the necessary info about the stock to be
    displayed on the visualization page.

    The instance method getHist returns the close price history for the desired period.
 """

import yfinance as yf  # yfinance library to collect data
import plotly.graph_objects as go  # plotly for graphing


class StockInfo:
    def __init__(self, set_ticker_name):
        """
        class creates object containing relevant info for desired stock
        :param tickerName: [string] stock ticker
        """
        # store ticker name
        self.ticker_name = set_ticker_name

        # create Ticker object
        self.ticker = yf.Ticker(self.ticker_name)

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

    def get_hist(self):
        """
        function retrieves close price history for desired stock
        :return: [pandas dataframe] dataframe of historical closing prices
        """

        # get historical data. available periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. default = 1mo
        historical = self.ticker.history(period="max")

        # remove unnecessary columns
        historical = historical.drop(columns=['Volume', 'Dividends', 'Stock Splits'])

        # reset index and make Date a column
        historical = historical.reset_index()

        # add 7-day close moving average
        historical['MA'] = historical.Close.rolling(window=7).mean()

        return historical

    def plot_hist(self):
        """
        function creates FigureWidget showing candlestick and moving average plots of desired stock
        :return: void
        # TODO: return figure object?
        """
        hist = self.get_hist()

        candle = go.Candlestick(
            x=hist['Date'],
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='Candlestick'
        )

        avg = go.Scatter(
            x=hist['Date'],
            y=hist['MA'],
            name='moving average'
        )

        # Add range slider
        layout = dict(
            title=self.name + ' (' + self.ticker_name + ')',
            yaxis_title='Stock Price (USD)',

            # range selection buttons stuff
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        data = [candle, avg]

        # used FigureWidget to try to implement x-axis autoscale. will revert back to Figure if unable.
        fig = go.FigureWidget(data=data, layout=layout)

        # TODO: yaxis autoscale
        # [INOP] autoscale y-axis on x-axis range change
        # def zoom(layout, xrange):
        #     in_view = hist.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
        #     fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]
        #
        #
        # fig.layout.on_change(zoom, 'xaxis.range')

        # necessary to show FigureWidget object
        fig.show(renderer="browser")

# example code
google = StockInfo("goog")

googlehist = google.plot_hist()
