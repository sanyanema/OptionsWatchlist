import yfinance as yf
import matplotlib.pyplot as plt

goog = yf.Ticker("GOOG")

option = goog.history(period='max')

print(option)