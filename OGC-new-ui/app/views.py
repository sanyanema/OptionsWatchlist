# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import yfinance
from django.views.decorators.csrf import csrf_protect
from wallstreet import Call, Put
from . import stock_info, options_info, greek_options, converter, trendingtickers
from django.contrib.auth.models import User
from .models import Transaction, Account
import json
import pandas as pd
import re


@login_required(login_url="/login/")
def index(request):
    trending = trendingtickers.getTrendingTickers()
    gainers = trendingtickers.getBiggestGainers()
    losers = trendingtickers.getBiggestLosers()
    account = Account.objects.get(user_id=request.user.get_username())
    watchlist = account.watchlist.split(',')
    
    return render(request, "index.html", {'trending': trending,
                                          'gainers': gainers,
                                          'losers': losers,
                                          'watchlist': watchlist})


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
def tables(request, ticker):

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
    expirationDate = request.GET.get('expirationDates','')

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

    return render(request, "ui-tables_tickers.html", {
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


def maps(request, ticker):
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

    account = Account.objects.get(user_id=request.user.get_username())
    startingwatchlist = account.watchlist.split(',')
    isInWatchlist = ticker in startingwatchlist

	# Adding stock to watchlist functionality
    if request.method == "GET":
        watchlistTicker = ticker
        account = Account.objects.get(user_id=request.user.get_username())
        if watchlistTicker not in account.watchlist:
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

    return render(request, "ui-maps_tickers.html", {
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
        'watchlist': watchlist,
        'inWatchlist': isInWatchlist
    })

def contract(request, contract):
    try: 
        option = options_info.getOptionInfoFromContract(contract)
        ticker = option['ticker']
        date = option['expirationDate']
        optionType = option['type']
        strike = option['strike']

        index_number = re.search(r"\d", contract)
        ticker = contract[0 : index_number.start()]
        stock = stock_info.StockInfo(ticker)
        name = stock.name

        if optionType is "Call":
            delta, gamma, rho, vega, theta = greek_options.getGreeks(greek_options.yFinanceToWallStreet(yfinance.Ticker(ticker).option_chain(date).calls, strike))
        else: 
            delta, gamma, rho, vega, theta = greek_options.getGreeks(greek_options.yFinanceToWallStreet(yfinance.Ticker(ticker).option_chain(date).puts, strike))
    except: 
        context = {}
        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))
    
    if 'Buy' in request.POST:
        
    elif 'Sell' in request.POST:

    transaction = Transaction(transaction_ID=,expiration_date=,contract_symbol=,stock=,purchase_price=,quantity=100)
    transaction.save(force_insert=True)
    transaction.full_clean()
    account = Account.objects.get(user_id=request.user.get_username())
    account.transaction.add(transaction)
    account.save()
    account.full_clean()

    return render(request, "contract.html", {
        'contract' : contract,
        'delta': round(delta,5),
        'gamma': round(gamma,5),
        'rho': round(rho,5),
        'vega': round(vega,5),
        'theta': round(theta,5),
        'IV' : ticker,
        'name' : name,
        'option':option
    })
