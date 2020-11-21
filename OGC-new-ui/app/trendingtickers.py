import urllib3
from bs4 import BeautifulSoup

def getTrendingTickers():
    req = urllib3.PoolManager()
    res = req.request('GET', "https://finance.yahoo.com/trending-tickers")

    soup = BeautifulSoup(res.data, 'html.parser')

    names = soup.find('tbody', {'class': ''}).findAll('td',{'class': "data-col1 Ta(start) Pstart(10px) Miw(180px)"})

    change = soup.find('tbody',{'class': ''}).findAll('span')
    companies = [];
    amounts = [];
    trending = dict();

    for company in names:
        name = (str(company).replace('<td class="data-col1 Ta(start) Pstart(10px) Miw(180px)"',''))
        name = name.replace('</td>','')
        index = name.find('>')
        name = name[index+1:len(name)]
        companies.append(name);
    for amt in change:
        if '%' in str(amt):
            amount = str(amt).replace('class="data-col4 Ta(end) Pstart(20px)"','')
            amount = amount.replace('</span>','')
            index = amount.find('>')
            amount = amount[index+1:len(amount)]
            amounts.append(amount)
    if len(companies) == len(amounts):
        for x in range(0,len(companies)):
            trending[companies[x]] = amounts[x]

    return trending


# print(getTrendingTickers())
