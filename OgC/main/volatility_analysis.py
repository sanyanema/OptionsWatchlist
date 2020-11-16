import yfinance as yf
from numpy import sqrt,mean,log,diff
from datetime import date
from tabulate import tabulate

#input: 'ticker', date 'YYYY-MM-DD', type 'calls' or 'puts'
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

    #calculate HV
    period = str(difference) + 'd'
    ticker_history = tick.history(period = period)
    price_history = ticker_history["Close"].tail(difference).tolist()
    r = diff(log(price_history))
    r_mean = mean(r)
    diff_square = [(r[i] - r_mean) ** 2 for i in range(0, len(r))]
    std = sqrt(sum(diff_square) * (1.0 / (len(r) - 1)))
    historical_vol = std * sqrt(difference)

    print(historical_vol)

    #determine puts or calls
    if type == 'puts':
        options = chain.puts
        print("options = puts")
    elif type == 'calls':
        options = chain.calls
        print("options = calls")

    #create list of over/under valued for each options contract
    valued = [None] * len(options.index)
    implied_vol = options["impliedVolatility"]

    for i in range(0, len(options.index)):
        if float(implied_vol[i]) >= historical_vol:
            valued[i] = "over"
        elif float(implied_vol[i]) < historical_vol:
            valued[i] = "under"

    options['valued'] = valued #add list to options dataframe

    toReturn = options[['contractSymbol','strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'valued']].copy() #create dataframe of contracts and other information

    #test code for printing just over or undervalued contracts
    #for i in range(0, len(contracts_and_valued.index)):
    #    if contracts_and_valued['valued'][i] == "over" :
    #        tuple = (contracts_and_valued['contractSymbol'][i], contracts_and_valued['valued'][i])
    #        print(tuple)

    print(tabulate(toReturn, headers='keys', tablefmt='psql'))


<<<<<<< HEAD:volatility_analysis.py
overorunder('TSLA', '2020-11-20 ', 'calls')
=======
overorunder('AMZN', '2020-11-13', 'calls')
>>>>>>> master:OgC/main/volatility_analysis.py
