import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from stock_info import StockInfo

ticker = "GOOG"

stock = StockInfo(ticker)
hist = stock.get_hist("max")
print(hist)

fig = go.Figure(data=[go.Candlestick(
    x=hist['Date'],
    open=hist['Open'],
    high=hist['High'],
    low=hist['Low'],
    close=hist['Close'],
    name='Candlestick'
)])

fig.add_trace(go.Scatter(
    x=hist['Date'],
    y=hist['MA'],
    name='moving average'
))

# Add range slider
fig.update_layout(
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

fig.update_layout(
    title=stock.name + ' (' + ticker + ')',
    yaxis_title='Stock Price (USD)',
)


fig.show()
