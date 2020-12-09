from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import yfinance
from django.views.decorators.csrf import csrf_protect
from wallstreet import Call, Put
from . import stock_info, options_info, greek_options, converter, trendingtickers, screener, watchlistDisplay,volatility_analysis
from django.contrib.auth.models import User
from .models import Transaction, Account
from django.db.models import F
import json
import pandas as pd
import re


@login_required(login_url="/login/")
def index(request):
    trending = trendingtickers.getTrendingTickers()
    gainers = trendingtickers.getBiggestGainers()
    losers = trendingtickers.getBiggestLosers()
    account = Account.objects.get(user_id=request.user.get_username())
    balance = account.balance
    contracts = {t.contract_symbol : t.contract_symbol for t in account.transaction.all() }.values()
    holdings = dict()
    total = 0
    numCalls = 0
    numPuts = 0
    for contract in contracts:
        transactions = account.transaction.filter(contract_symbol=contract)
        quantity = sum([t.quantity for t in transactions])
        if quantity == 0:
            continue
        option = options_info.getOptionInfoFromContract(contract)
        ticker = option['ticker']
        date = option['expirationDate']
        optionType = option['type']
        strike = option['strike']
        index_number = re.search(r"\d", contract)
        ticker = contract[0: index_number.start()]
        stock = stock_info.StockInfo(ticker)
        name = stock.name
        price = 0
        if optionType == "Call":
            numCalls += 1
            dates = greek_options.dateConverter(date)
            call = Call(ticker,
                        d=dates[2], m=dates[1], y=dates[0],
                        strike=strike, source='yahoo')
            price = call.price
        else:
            numPuts += 1
            dates = greek_options.dateConverter(date)
            put = Put(ticker,
                        d=dates[2], m=dates[1], y=dates[0],
                        strike=strike, source='yahoo')
            price = put.price
        current_price = price
        
        profit = round(sum([t.quantity * (current_price - t.purchase_price) for t in transactions]),2)
        owned = quantity * current_price
        total += owned
        balance += total
        holdings[contract] = {'current_price':current_price, 'quantity':quantity, 'portfolio_share':owned, 'profit':profit}
    watchlist = account.watchlist.split(',')
    total_contracts = 0
    for holding in holdings:
        holdings[holding]['portfolio_share'] = round(holdings[holding]['portfolio_share'] / total * 100, 2)
        total_contracts += holdings[holding]['quantity']
    inform = watchlistDisplay.getWatchListInfo(watchlist)
    balance = round(balance, 2)
    return render(request, "index.html", {'trending': trending,
                                          'gainers': gainers,
                                          'losers': losers,
                                          'watchlist': watchlist,
                                          'info': inform,
                                          'holdings': holdings,
                                          'balance': balance,
                                          'contractTotal': total_contracts,
                                          'numCalls' : numCalls,
                                          'numPuts' : numPuts})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))


@csrf_protect
@login_required(login_url="/login/")
def options(request, ticker):
    try:
        stock = stock_info.StockInfo(ticker.upper())
    except:
        try:
            ticker = converter.convert(ticker)
            stock = stock_info.StockInfo(ticker.upper())
        except:
            context = {}
            html_template = loader.get_template('error-404.html')
            return HttpResponse(html_template.render(context, request))

    name = stock.name
    image_draft = name.split()
    image = image_draft[0].split(".")

    # Expiration Dates
    dates = options_info.getExpirationDates(ticker)

    # Options Information
    expirationDate = ""
    # Blank table
    options = pd.DataFrame(
        columns=['Contract', 'Strike', 'Last Price', 'Implied Volatility', 'Expiration Date', 'Type Of Option'])

    # Differentiate based on radio input
    expirationDate = request.GET.get('expirationDates', '')

    if request.GET.get('type', "") == "Puts":
        options = options_info.findGreekData(options_info.getPuts(ticker, expirationDate))
    elif request.GET.get('type', "") == "Calls":
        options = options_info.findGreekData(options_info.getCalls(ticker, expirationDate))
    else:
        pass

    # Format dataframe for html
    optionsData = options.to_dict(orient="records")

    options_html = options.to_html()
    option_price_draft = stock.current_price.split()
    option_price = float(option_price_draft[0])

    # Greeks
    try:
        delta, gamma, rho, vega, theta = greek_options.getGreeks(
            greek_options.yFinanceToWallStreet(yfinance.Ticker(ticker).option_chain("2020-11-20").calls, option_price))
    except:
        delta, gamma, rho, vega, theta = ["NA", "NA", "NA", "NA", "NA"]

    return render(request, "options_stock.html", {
        'name': name,
        'ticker': ticker.upper(),
        'options': optionsData,
        'price': stock.current_price,
        'day_range': stock.day_range,
        '52wk_range': stock.yr_range,
        'volume': stock.avg_volume,
        'eps': stock.eps_trail,
        'market_cap': stock.market_cap,
        'industry': stock.sector,
        'delta': delta,
        'gamma': gamma,
        'rho': rho,
        'vega': vega,
        'theta': theta,
        'dates': dates,
        'image': image[0],
    })


def stock(request, ticker):
    try:
        stock = stock_info.StockInfo(ticker.upper())
    except:
        try:
            ticker = converter.convert(ticker)
            stock = stock_info.StockInfo(ticker.upper())
        except:
            context = {}
            html_template = loader.get_template('error-404.html')
            return HttpResponse(html_template.render(context, request))
    # Stock Price Chart
    name = stock.name
    plot_html = stock.plot_hist()
    image_draft = name.split()
    image = image_draft[0].split(".")
    current_user = request.user
    undervalued_growth, day_gainer, day_loser, most_active, undervalued_large_cap, small_momentum = screener.screener(ticker)

    account = Account.objects.get(user_id=request.user.get_username())
    startingwatchlist = account.watchlist.split(',')
    isInWatchlist = ticker in startingwatchlist

    # Adding stock to watchlist functionality
    if request.GET.get("watchlist") is not None:
        watchlistTicker = ticker
        account = Account.objects.get(user_id=request.user.get_username())
        if account.watchlist == "":
            setattr(account, 'watchlist', watchlistTicker)
            watchlist = watchlistTicker
            account.save()
        elif watchlistTicker not in account.watchlist:
            ticker_list = account.watchlist.split(',')
            ticker_list.append(watchlistTicker)
            watchlist = ','.join(ticker_list)
            setattr(account, 'watchlist', watchlist)
            account.save()
        else:
            ticker_list = account.watchlist.split(',')
            ticker_list.remove(watchlistTicker)
            watchlist = ','.join(ticker_list)
            setattr(account, 'watchlist', watchlist)
            account.save()

    account = Account.objects.get(user_id=request.user.get_username())
    endingwatchlist = account.watchlist.split(',')
    isInWatchlist = ticker in endingwatchlist

    return render(request, "stock.html", {
        'name': name,
        'price': stock.current_price,
        'day_range': stock.day_range,
        '52wk_range': stock.yr_range,
        'volume': stock.avg_volume,
        'eps': stock.eps_trail,
        'market_cap': stock.market_cap,
        'industry': stock.sector,
        'ticker': ticker.upper(),
        'plot_html': plot_html,
        'image': image[0],
        'inWatchlist': isInWatchlist,
        'undervalued_growth' : undervalued_growth,
        'day_gainer' : day_gainer,
        'day_loser' : day_loser,
        'most_active' : most_active,
        "undervalued_large_cap" : undervalued_large_cap,
        "small_momentum" : small_momentum,
    })


def contract(request, contract):
    typ = ""

    try:
        option = options_info.getOptionInfoFromContract(contract)
        ticker = option['ticker']
        date = option['expirationDate']
        optionType = option['type']
        strike = option['strike']

        index_number = re.search(r"\d", contract)
        ticker = contract[0: index_number.start()]
        stock = stock_info.StockInfo(ticker)
        name = stock.name
        amount = request.GET.get("quantity","")
    
    
        
        if optionType == "Call":
            delta, gamma, rho, vega, theta = greek_options.getGreeks(
                greek_options.yFinanceToWallStreet(yfinance.Ticker(ticker).option_chain(date).calls, strike))
            dates = greek_options.dateConverter(date)
            call = Call(ticker,
                        d=dates[2], m=dates[1], y=dates[0],
                        strike=strike, source='yahoo')
            price = call.price
            typ = "Call"
        else:
            delta, gamma, rho, vega, theta = greek_options.getGreeks(
                greek_options.yFinanceToWallStreet(yfinance.Ticker(ticker).option_chain(date).puts, strike))
            dates = greek_options.dateConverter(date)
            put = Put(ticker,
                        d=dates[2], m=dates[1], y=dates[0],
                        strike=strike, source='yahoo')
            price = put.price
            typ = "Put"
    except:
        context = {}
        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    account = Account.objects.get(user_id=request.user.get_username())
    if request.GET.get('type', "") == "Buy":
        # TODO type of option, strike
        transaction = Transaction(expiration_date=date,contract_symbol=contract,purchase_price=price,quantity=amount,typ=typ,strike=strike)
        transaction.save(force_insert=True)
        transaction.full_clean()
        account.balance -= int(price * float(int(amount)) *float(100))
        account.save()
        account.transaction.add(transaction)
        transactions = account.transaction.filter(contract_symbol=contract)
        try:
            quantity = sum([t.quantity for t in transactions])
            
        except:
            # TODO: Change this to "you cannot sell because you do not own the stock"
            context = {}
            html_template = loader.get_template('error-404.html')
            return HttpResponse(html_template.render(context, request))

    elif request.GET.get('type', "") == "Sell":
        transactions = account.transaction.filter(contract_symbol=contract)
        try:
            transaction = transactions[0]
            transaction.pk = None

        except:
            # TODO: Change this to "you cannot sell because you do not own the stock"
            context = {}
            html_template = loader.get_template('error-404.html')
            return HttpResponse(html_template.render(context, request))
        transaction.save(force_insert=True)
        transaction.full_clean()
        transaction.quantity = int(amount) * -1
        transaction.save()
        transaction.full_clean()
        account.balance += int(price * float(int(amount)) * float(100))
        account.save()
        account.transaction.add(transaction)
        quantity = sum([t.quantity for t in transactions])
    else:
        pass
    account.save()
    account.full_clean()

    valuation = volatility_analysis.overorunder(ticker, date, optionType)[contract]
    quantity = sum([t.quantity for t in account.transaction.filter(contract_symbol=contract)])
    return render(request, "contract.html", {
        'contract': contract,
        'delta': round(delta, 5),
        'gamma': round(gamma, 5),
        'rho': round(rho, 5),
        'vega': round(vega, 5),
        'theta': round(theta, 5),
        'IV': ticker,
        'name': name,
        'option': option,
        'price': price,
        'quantity': quantity,
        'valuation' : valuation
    })
