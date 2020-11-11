""" This file defines the class StockInfo.

    A new instance of StockInfo contains the necessary info about the stock to be
    displayed on the visualization page.

    The instance method git_hist returns the close price history for the maximum period.

    The instance method plot_hist displays a candlestick plot with moving average and Bollinger Band overlays.
 """

import yfinance as yf  # yfinance library to collect data
import plotly.graph_objects as go  # plotly for graphing
from candlestick import candlestick #import pattern recognition


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

    def pattern(self):

        # get historical data. available periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. default = 1mo
        history = self.ticker.history(period="max")

        # remove unnessessary columns
        dates = history[['Open','High','Low','Close']]

        # rename columns for use with candlestick pattern library
        dates.rename(columns = {"Open":"open","High":"high","Low":"low","Close":"close"}, inplace = True)

        # dictionary of patterns. TODO: make it so that different patterns are selectable
        patternDict = {
            "inverted_hammer": candlestick.inverted_hammer(dates, target="output"),
            "doji_star": candlestick.doji_star(dates, target="output"),
            "bearish_harami": candlestick.bearish_harami(dates, target="output"),
            "bullish_harami": candlestick.bullish_harami(dates, target="output"),
            "dark_cloud_cover": candlestick.dark_cloud_cover(dates, target="output"),
            "doji": candlestick.doji(dates, target="output"),
            "dragonfly_doji": candlestick.dragonfly_doji(dates, target="output"),
            "hanging_man": candlestick.hanging_man(dates, target="output"),
            "gravestone_doji": candlestick.gravestone_doji(dates, target="output"),
            "bearish_engulfing": candlestick.bearish_engulfing(dates, target="output"),
            "bullish_engulfing": candlestick.bullish_engulfing(dates, target="output"),
            "hammer": candlestick.hammer(dates, target="output"),
            "morning_star_doji": candlestick.morning_star_doji(dates, target="output"),
            "piercing_pattern": candlestick.piercing_pattern(dates, target="output"),
            "rain_drop": candlestick.rain_drop(dates, target="output"),
            "rain_drop_doji": candlestick.rain_drop_doji(dates, target="output"),
            "star": candlestick.star(dates, target="output"),
            "shooting_star": candlestick.shooting_star(dates, target="output")
        }
        
        candles_df = patternDict["hammer"]

        #create list of indicies of True dates

        true_index = candles_df.index[candles_df['output'] == True].tolist()
        false_index = candles_df.index[candles_df['output'] == False].tolist()

        for_highlight = candles_df.copy(deep=True)

        for_highlight = for_highlight[~for_highlight.index.isin(false_index)]

        return for_highlight


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
            yaxis='y2',
            name='Candlestick'
        )

        avg = go.Scatter(
            x=hist['Date'],
            y=hist['20 Day MA'],
            yaxis='y2',
            name='moving average'
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

        for_highlight = self.pattern()

        highlighted_pattern = go.Candlestick(
        x=for_highlight.index,
            open=for_highlight['open'],
            high=for_highlight['high'],
            low=for_highlight['low'],
            close=for_highlight['close'],
            increasing={'line': {'color': '#0DF9FF'}},
            decreasing={'line': {'color': '#511CFB'}},
            name='highlight'
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
        data = [lower, upper, candle, avg, highlighted_pattern]

        # define figure
        fig = go.Figure(data=data, layout=layout)

        # display figure
        fig.show(renderer="browser")


# example code
stock = StockInfo("ZM")

stock.plot_hist()
