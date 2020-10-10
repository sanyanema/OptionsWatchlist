import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from stock_info import StockInfo

ticker = "GOOG"

stock = StockInfo(ticker)
hist = stock.get_hist("max")
print(hist)

fig = go.Figure(data=[go.Candlestick(
    x=      hist['Date'],
    open=   hist['Open'],
    high=   hist['High'],
    low=    hist['Low'],
    close=  hist['Close'])])

fig.update_layout(
    title=stock.name + ' (' + ticker + ')',
    yaxis_title='Stock Price (USD)',
    xaxis_rangeslider_visible=False
)

fig.show()