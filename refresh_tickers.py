"""
File fetches stock symbols listed on Nasdaq and 'Others' (as defined by Nasdaq FTP) from the Nasdaq FTP server
@ ftp://ftp.nasdaqtrader.com/SymbolDirectory/
"""

import urllib.request as request
import shutil
from contextlib import closing
import re

base_url = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/'
nasdaq_url = 'nasdaqlisted.txt'
other_url = 'otherlisted.txt'


def get_tickers(file_name):
    base_url = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/'
    with closing(request.urlopen(base_url + file_name)) as r:
        with open(file_name, 'wb') as f1:
            shutil.copyfileobj(r, f1)

    with open('other.txt', 'r') as f2:
        data = f2.read()

    return parse_tickers(file_name, data)


def parse_tickers(file_name, data):
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


nasdaq = get_tickers(nasdaq_url)
other = get_tickers(other_url)
