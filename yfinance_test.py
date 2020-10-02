import yfinance as yf
import matplotlib.pyplot as plt

goog = yf.Ticker("GOOG")

option = goog.history(period='max')

# print(option.columns)
# print(option['Close'])
# print(option.index)
print(option.ticker)


# plt.plot(option['Date'],option['Close'])
# plt.show()