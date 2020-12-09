""" This file defines the class StockInfo.

    A new instance of StockInfo contains the necessary info about the stock to be
    displayed on the visualization page.

    The instance method git_hist returns the close price history for the maximum period.

    The instance method plot_hist displays a candlestick plot with moving average and Bollinger Band overlays.
 """

import yfinance as yf  # yfinance library to collect data
import plotly.graph_objects as go  # plotly for graphing


class StockInfo:
    def __init__(self, set_ticker_name):
        """
        class creates object containing relevant info for desired stock
        :param set_ticker_name: [string] stock ticker
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

        # add 20-day close moving average
        historical['20 Day MA'] = historical.Close.rolling(window=20).mean()

        # add 20-day MA STD
        historical['20 Day STD'] = historical.Close.rolling(window=20).std()

        # add Bollinger upper and lower bands
        historical['Upper Band'] = historical['20 Day MA'] + (historical['20 Day STD'] * 2)
        historical['Lower Band'] = historical['20 Day MA'] - (historical['20 Day STD'] * 2)

        return historical

    def plot_hist(self):
        """
        function creates FigureWidget showing candlestick and moving average plots of desired stock
        :return: void
        """
        hist = self.get_hist()

        candle = go.Candlestick(
            x=hist['Date'],
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            yaxis='y2',
            name='Candlestick'
        )

        avg = go.Scatter(
            x=hist['Date'],
            y=hist['20 Day MA'],
            yaxis='y2',
            name='Moving Average'
        )

        lower = go.Scatter(
            x=hist['Date'],
            y=hist['Lower Band'],
            legendgroup='Bollinger Band',
            name='Bollinger Band',
            line=dict(color='rgba(200,200,200,1)'),
            fill='none'
        )

        upper = go.Scatter(
            x=hist['Date'],
            y=hist['Upper Band'],
            legendgroup='Bollinger Band',
            showlegend=False,
            line=dict(color='rgba(200,200,200,1)'),
            fill='tonexty',
            fillcolor='rgba(200,200,200,0.5)',
        )

        # Add range slider
        layout = dict(
            title=self.name + ' (' + self.ticker_name + ')',
            yaxis_title='Stock Price (USD)',

            # main y axis
            yaxis=dict(
                range=[0, hist[['High', 'Upper Band']].max().max() * 1.1]
            ),

            # second y axis for Bollinger Bands in background
            yaxis2=dict(
                overlaying='y',
                range=[0, hist[['High', 'Upper Band']].max().max() * 1.1]
            ),

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

        # define trace array to plot
        data = [lower, upper, candle, avg]

        # define figure
        fig = go.Figure(data=data, layout=layout)

        # get html
        plot_html = fig.to_html(full_html=False, include_plotlyjs=False)

        return plot_html
