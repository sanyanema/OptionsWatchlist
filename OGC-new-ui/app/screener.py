import yfinance as yf

def screener(ticker_input):

    screener_dict = {
        'undervalued_growth': False,
        'day_gainer': False,
        'day_loser': False,
        'most_active': False,
        'undervalued_large_cap': False,
        'small_momentum': False
    }

    ticker = yf.Ticker(ticker_input)
    info_dict = ticker.info

    #add keys if needed
    if 'trailingPE' not in info_dict:
        info_dict['trailingPE'] = None

    if 'pegRatio' not in info_dict:
        info_dict['pegRatio'] = None

    if 'forwardPE' not in info_dict:
        info_dict['forwardPE'] = None

    if 'sharesOutstanding' not in info_dict:
        info_dict['sharesOutstanding'] = None

    if 'previousClose' not in info_dict:
        info_dict['previousClose'] = None

    if 'ask' not in info_dict:
        info_dict['ask'] = None

    if 'volume' not in info_dict:
        info_dict['volume'] = None
   
    #check to make sure values are non-null
    if info_dict['volume'] != None:
        #if more than 50,000,000 shares have been traded: most_active = True
        if info_dict['volume'] > 50000000:
            screener_dict['most_active'] = True

    if info_dict['trailingPE'] != None and info_dict['pegRatio'] != None and info_dict['forwardPE'] != None: 
        #if PEG < 1 that means that expected growth > P/E and it's undervalued
        #trailing P/E between 0-20 means that stock price is trading at 0-20x it's trailing earnings per share
        #if forward P/E < trailing P/E that means investors think the stock will not keep up with growth
        #So essentially looking for when the data suggests investors are wrong about forward P/E
        if info_dict['trailingPE'] > 0 and info_dict['trailingPE'] < 20 and info_dict['pegRatio'] < 1 and info_dict['forwardPE'] < info_dict['trailingPE']:
            screener_dict['undervalued_growth'] = True

        market_cap = None
        intraday_change = None
        if info_dict['sharesOutstanding'] != None and  info_dict['previousClose'] != None:
            #Define market capitalization for that day
            market_cap = info_dict['sharesOutstanding'] * info_dict['previousClose']  
        
        if info_dict['ask'] != None and info_dict['previousClose'] != None:
            #percent change in price from previous close to current ask
            intraday_change = ((info_dict['ask'] - info_dict['previousClose']) / info_dict['previousClose']) * 100

        if market_cap != None and intraday_change != None:
            #if PEG < 1 that means that expected growth > P/E and it's undervalued
            #trailing P/E between 0-20 means that stock price is trading at 0-20x it's trailing earnings per share
            #market cap between10,000,000,000 and 200,000,000,000 = large market capitalization
            if info_dict['trailingPE'] > 0 and info_dict['trailingPE'] < 20 and info_dict['pegRatio'] < 1 and market_cap > 10000000000 and market_cap < 200000000000:
                screener_dict['undervalued_large_cap'] = True        
            
            #Sizeable upwards change in price for a middle market capitizization or bigger stock
            if intraday_change > 3 and market_cap > 2000000000 and info_dict['volume'] > 15000:
                screener_dict['day_gainer'] = True

            #Sizeable downwards change in price for a middle market capitizization or bigger stock
            if intraday_change < -2.5 and market_cap > 2000000000 and info_dict['volume'] > 20000:
               screener_dict['day_loser'] = True
            
            #Small market capitalization stock with >5% change in price today
            if intraday_change > 5 and market_cap > 200000000 and market_cap < 2000000000:
                screener_dict['small_momentum'] = True

    # return screener_dict
    undervalued_growth = screener_dict['undervalued_growth']
    day_gainer = screener_dict['day_gainer']
    day_loser = screener_dict['day_loser']
    most_active = screener_dict['most_active']
    undervalued_large_cap = screener_dict['undervalued_large_cap']
    small_momentum = screener_dict['small_momentum']
    return undervalued_growth, day_gainer, day_loser, most_active, undervalued_large_cap, small_momentum

# print(screener('EXPR'))
# print(screener('GOOG'))
# print(screener('AAPL'))
# print(screener('MSFT'))
