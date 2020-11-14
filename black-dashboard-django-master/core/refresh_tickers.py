"""
==================================================================================================================
This file is useless. For a complete list of tickers valid as of October 18th 2020, see file tickers.txt
==================================================================================================================

File fetches stock symbols listed on Nasdaq and 'Others' (as defined by Nasdaq FTP) from the Nasdaq FTP server
@ ftp://ftp.nasdaqtrader.com/SymbolDirectory/

Note: while the obtained tickers are listed on the Nasdaq FTP server, they are not necessarily available from
the yfinance library.
"""

import urllib.request as request
import re


def get_tickers(file_name):
    """
    this method returns a list of tickers from a published txt file on the specified nasdaq ftp server
    :param file_name: name of published file
    :return: list of tickers in published file
    """

    base_url = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/'

    # get data from ftp server
    response = request.urlopen((base_url + file_name))
    data = response.read()

    # convert data from byte to string
    data = data.decode("utf-8")

    # call parse_tickers to get tickers from data string
    tickers = parse_tickers(file_name, data)

    return tickers


def parse_tickers(file_name, data):
    """
    this method goes through the data string and parses the tickers
    :param file_name: published txt file
    :param data: string containing tickers
    :return: list of tickers
    """
    tickers = []
    lines = data.split('\n')

    # retrieve ticker symbol and add to tickers array
    for line in lines[1:-2]:
        tickers.append(line.split('|')[0])

    # display when the ticker list was last updated by Nasdaq
    timestamp = lines[-2]
    pattern = r'(?P<month>\d{2})(?P<day>\d{2})(?P<year>\d{4})(?P<time>\d{2}:\d{2})'
    result = re.search(pattern, timestamp)
    month, day, year, time = result.group(1), result.group(2), result.group(3), result.group(4)
    print('Ticker list \'' + file_name + '\' last updated on: ' + month + '/' + day + '/' + year + ' ' + time)

    # return ticker symbols
    return tickers


nasdaq_url = 'nasdaqlisted.txt'
other_url = 'otherlisted.txt'

nasdaq = get_tickers(nasdaq_url)
other = get_tickers(other_url)
