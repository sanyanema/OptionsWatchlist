import yfinance as yf
from numpy import sqrt,mean,log,diff,std
from datetime import date

#input: ticker, date (YYYY-MM-DD), type {all strings}
def overorunder(ticker, expiration_date, type):
    """
    :param ticker: String from the following markets:
    :param expiration_date: String in the format YYYY-MM-DD
    :param type: 'puts' or 'calls'
    :return: pandas df that has two columns: contract name and over or undervalued

    Over or undervalued is determined by comparing historical volatility to the implied volatility of each contract
    HV is calcuated using stock close price for X days before current date if option expires in X days.
    i.e. if option expires in 13 days, HV is calculated using 13 past days of data

    If HV >= IV, undervalued
    If HV < IV, overvalued
    """
    tick = yf.Ticker(ticker)

    chain = tick.option_chain(expiration_date) #create option chain


    #determine puts or calls
    if type == 'Put':
        options = chain.puts
    elif type == 'Call':
        options = chain.calls

    #date not in ticker.options, raise error
    try:
        expiration_date in tick.options
    except:
        print("date must be in list of option expiry dates in format 'YYYY-MM-DD'")

    # find difference of today's date and expire date
    exp_date = expiration_date.split('-')
    end_date = date(int(exp_date[0]), int(exp_date[1]), int(exp_date[2]))
    today = date.today()
    days_between = end_date - today
    difference = days_between.days

    ticker_history = tick.history(period = "1y")
    #HV calculated over 2*period until option expieration to try to get rid of noise
    price_history = ticker_history["Close"].tail(difference*2).tolist()
    returns = []
    #calculate daily returns over the period and then apply ln to normalize.
    for i in range(1, len(price_history)):
        returns.append(log(price_history[i]/price_history[i-1]))

    avg_return = mean(returns)
    #next two lines calculate standard deviation and them multiply by sqrt(period length)
    diff_square = [(returns[i]-avg_return)**2 for i in range(0, len(returns))]
    historical_vol = sqrt(sum(diff_square)*(1.0/(len(returns)-1))) * sqrt(len(price_history))

    #create dictionary of over/under valued for each options contract
    valued = {}
    #valued = [None] * len(options.index)
    implied_vol = options['impliedVolatility']
    contracts = options['contractSymbol']

    #over or under valued if 0.5*HV > IV > 1.5*HV
    #else: None
    for i in range(0, len(options.index)):
        if float(implied_vol[i]) >= historical_vol + 0.5*historical_vol:
            valued[contracts[i]] = 'Over'
        elif float(implied_vol[i]) <= historical_vol - 0.5*historical_vol:
            valued[contracts[i]] = 'Under'
        else:
            valued[contracts[i]] = None

    return valued


# print(overorunder('GE', '2021-01-15', 'Put'))
