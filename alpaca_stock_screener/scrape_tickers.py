import bs4 as bs
import pickle
import requests
import re


def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker.replace('\n', ''))

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers

def save_etfs():
    # Make a request to the website
    r = requests.get('https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds')

    # Parse the page
    soup = bs.BeautifulSoup(r.text, 'html.parser')

    # Find the div containing the ETFs list
    content_div = soup.find('div', {'id': 'mw-content-text'})

    # Define the headers corresponding to the sections we're interested in
    headers = ['Broad market ETFs', 'Index-tracking ETFs', 'Large-cap ETFs', 'Leveraged ETFs', 'Leveraged short ETFs', 'Short ETFs', 'Precious metals ETFs']

    symbols = []
    # Iterate over the headers
    for header in headers:
        # Find the header (span tag within h3 tag) with the matching text
        span = content_div.find('span', {'class': 'mw-headline'}, string=lambda text: text and header in text)

        if span:
            # Find the next sibling of the header's parent (h3 tag) that is a list (ul tag)
            ul = span.parent.find_next_sibling('ul')

            # Iterate over the list items in this list
            for li in ul.find_all('li'):
                # Extract and print the ETF name and ticker
                etf = li.text.strip()
                matches = re.findall(r'\(([^\)]*)\)', etf)
                if matches:
                    symbol = re.split(r'\s|\|', matches[-1])[-1]
                    symbols.append(symbol.replace('\n', ''))

    with open("etfs.pickle", "wb") as f:
        pickle.dump(symbols, f)

    return symbols


def dump_all():
    symbols = ['VIXY']  # wasnt in the list from wikipedia
    symbols += save_sp500_tickers()
    symbols += save_etfs()
    with open("sp500andETFs.pickle", "wb") as f:
        pickle.dump(symbols, f)
    return symbols


if __name__ == '__main__':
    dump_all()