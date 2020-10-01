import yfinance as yf

goog = yf.Ticker("GOOG")

option = goog.option_chain('2020-10-09')

print(option[0]['ask'])