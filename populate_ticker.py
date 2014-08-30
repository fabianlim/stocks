import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks.settings')

from django.db import models

from ticker.models import Ticker, Quote, Historical
from ticker.query import QueryInterface

import datetime

def sparse_entries():
# main will not really run because of paths problems
# add the ticker
    tick =Ticker.objects.get_or_create(symbol="GOOG",
            name="Google Inc",
            industry="internet",
            industry_id=100)[0]

    print tick.id
    print Ticker.objects.all()

#add the quote
    tm = datetime.time(10,20,30)
    dt = datetime.date(2014,10,24)

    tick.quote_set.create(date=datetime.date(2014,10,24), #yr, mt, day
            time=datetime.time(8,20,30), #hr, min, sec
            change=+0.1,
            ask=582.1)

    tick.quote_set.create(date=datetime.date(2014,10,24), #yr, mt, day
            time=datetime.time(10,20,30), #hr, min, sec
            change=-0.81,
            ask=582.65)

    quote = tick.quote_set.create(date=datetime.date(2014,10,25), #yr, mt, day
            time=datetime.time(10,20,30), #hr, min, sec
            change=+0.6,
            ask=583)

    print tick.quote_set.all() # get allthe quotes with ticker=tick
    print Quote.objects.filter(ticker__symbol='GOOG') # ticker is Foreign key here
    print Quote.objects.filter(date__day=25)

# add some historic entries to 'GOOG' ticker
def historic_entries():
    tick = Ticker.objects.get(symbol='GOOG')
    query_results = QueryInterface.query_historicaldata("*", "GOOG")
    Ticker.query_to_models('GOOG', query_results.results, model=Historical)

# download all tickers
def ticker_entries(company_filter_tag=None):
    # filter with tag (if provided)
    ticks_by_industry = QueryInterface.query_tickers(company_filter_tag)
    # ticks_by_industry will be a list of dictionaries
    # each dictionary (industry) will have keys
    # company:
    # name:
    # id:
    for industry in ticks_by_industry:
        # if a valid dict with comapies
        if 'company' in industry.keys():
            # should be a list of companies
            companies = industry['company']
            # if a singleton need to make a list
            if not isinstance(companies, list):
                companies = [companies]
            # iterate through, each entry is a company
            for entry in companies:
                print entry
                try:
                    Ticker.objects.get_or_create(symbol=entry['symbol'],
                            name=entry['name'],
                            industry=industry['name'],
                            industry_id=industry['id'])
                except Exception as e:
                    print e
            print """Added {} entries
                in industry {}""".format(len(industry['company']),
                        industry['name'])

# add an arbitrary SG quote for testing
def add_sg_quote():

    # add an arbitrary SG ticker
    ticker = 'S68.SI' #singapore exchange
    t = Ticker.objects.get_or_create(symbol=ticker,
            name="Google Inc",
            industry="internet",
            industry_id=100)

    # clear all the existing quotes
    Quote.objects.all().delete()
    q = QueryInterface.query_quote(','.join(Quote.get_fields()), ticker)
    Ticker.query_to_models(ticker, q.results, Quote)

# search through all tickers in SG market and pull them off the web
def pull_sg_quotes():
    # go for SG tickers
    for t in Ticker.objects.filter(symbol__contains='.SI').all():
        q = QueryInterface.query_quote(','.join(Quote.get_fields()), t.symbol)
        try:
            Ticker.query_to_models(t.symbol, q.results, Quote)
            print "{}: quote {}:{} successfull added!".format(t.symbol,
                    q.date,
                    q.time)
        except Exception as e:
            print "{} : caught exception! : {}".format(t.symbol, e)

# print the top 5 tickers with the most quotes
def top_five_most_quotes():
    for ticker in sorted([(len(t.quote_set.all()), t) for t in Ticker.objects.all()],
            reverse=True)[:5]:
        print ticker[1].quote_set.all()

if __name__ == '__main__':
    funcs = {'sparse_entries': sparse_entries,
         'historic_entries': historic_entries,
         'ticker_entries' : ticker_entries,
          'add_sg_quote' : add_sg_quote,
          'pull_sg_quotes' : pull_sg_quotes,
          'top_five_most_quotes': top_five_most_quotes}

    import argparse

    parser = argparse.ArgumentParser(description='helper scripts ... etc...')
    parser.add_argument('fname', help='name of function to call')
    parser.add_argument('argv1', nargs='?', help='extra argument to function')
    args = parser.parse_args()

    # call the function
    if args.argv1:
        funcs[args.fname](args.argv1)
    else:
        funcs[args.fname]()



