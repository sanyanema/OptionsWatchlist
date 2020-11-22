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
from .models import Stock, Transaction, Account
import json
import pandas as pd


@login_required(login_url="/login/")
def index(request):
    trending = trendingtickers.getTrendingTickers()
    gainers = trendingtickers.getBiggestGainers()
    losers = trendingtickers.getBiggestLosers()
    return render(request, "index.html", {'trending': trending,
                                          'gainers': gainers,
                                          'losers': losers})


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
    dates = json.dumps(options_info.getExpirationDates(ticker))

    # Options Information

    # Blank table
    options = pd.DataFrame(
        columns=['Contract', 'Strike', 'Last Price', 'Implied Volatility', 'Expiration Date', 'Type Of Option'])

    # Differentiate based on radio input
    if request.GET.get('type', "") == "Puts":
        options = options_info.findGreekData(options_info.getPuts(ticker, '2020-11-27'))
    elif request.GET.get('type', "") == "Calls":
        options = options_info.findGreekData(options_info.getCalls(ticker, '2020-11-27'))
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

	# Hard-coded adding stock to watchlist functionality
    if request.method == "POST":
        stock = Stock(name='WWW')
        stock.save(force_insert=True)
        stock.users.add(current_user)
        stock.save(force_insert=True)
        stock.full_clean()
    return render(request, "ui-maps_tickers.html", {
        'name': name,
        'ticker': ticker.upper(),
        'plot_html': plot_html,
        'image': image[0],
    })
