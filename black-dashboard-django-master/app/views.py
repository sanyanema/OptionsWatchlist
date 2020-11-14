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
from wallstreet import Call, Put
from . import stock_info, options_info, greek_options
import json
import pandas as pd

@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/ui-tables.html/")
def pages(request):
    # Options Information
    options = options_info.findGreekData(options_info.getCalls('GOOGL', '2020-11-20'))
    options_html = options.to_html()

    # Stock Price Chart
    stock = stock_info.StockInfo('GOOGL')
    plot_html = stock.plot_hist()

    # Greeks 
    delta, gamma, rho, vega, theta = greek_options.getGreeks(greek_options.yFinanceToWallStreet(yfinance.Ticker('GOOGL').option_chain("2020-11-20").calls, 2000))

    return render(request, "ui-tables.html", {
        'options' : options_html,
        'price' : stock.current_price,
        'day_range' : stock.day_range,
        '52wk_range' : stock.yr_range,
        'volume' : stock.avg_volume,
        'eps' : stock.eps_trail,
        'market_cap' : stock.market_cap,
        'industry' : stock.sector,
        'delta' : delta,
        'gamma' : gamma,
        'rho' : rho,
        'vega' : vega,
        'theta' : theta,
        })
