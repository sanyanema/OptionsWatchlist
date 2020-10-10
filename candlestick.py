import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from stock_info import StockInfo

google = StockInfo("GOOG")
googlehist = google.get_hist("6mo")
print(googlehist)

fig = go.Figure(data=[go.Candlestick(
    x=      googlehist['Date'],
    open=   googlehist['Open'],
    high=   googlehist['High'],
    low=    googlehist['Low'],
    close=  googlehist['Close'])])

fig.show()