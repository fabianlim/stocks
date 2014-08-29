import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks.settings')

from django.db import models
from ticker.models import Ticker, Quote, Historical

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

def historic_entries():
    tick = Ticker.objects.get(symbol='GOOG')
    from ticker.query import QueryInterface
    query_results = QueryInterface.query_historicaldata("*", "GOOG")
    Ticker.query_to_models('GOOG', query_results.results, model=Historical)

def ticker_entries():
    from ticker.query import QueryInterface
    # this gets tickers by industry
    ticks_by_industry = QueryInterface.query_tickers()
    #import pdb
    #pdb.set_trace()
    for industry in ticks_by_industry:
        if 'company' in industry.keys():
            companies = industry['company']
            if not isinstance(companies, list):
                companies = [companies]
            print companies
            for entry in companies:
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

def add_sg_quote():
    from ticker.query import QueryInterface
    from ticker.models import Ticker, Quote
    ticker = 'S68.SI' #singapore exchange
    t = Ticker.objects.get_or_create(symbol=ticker,
            name="Google Inc",
            industry="internet",
            industry_id=100)
    Quote.objects.all().delete()
    q = QueryInterface.query_quote(','.join(Quote.get_fields()), ticker)
    Ticker.query_to_models(ticker, q.results, Quote)

def pull_sg_quotes():
    from ticker.query import QueryInterface
    for t in Ticker.objects.filter(symbol__contains='.SI').all():
        q = QueryInterface.query_quote(','.join(Quote.get_fields()), t.symbol)
        try:
            Ticker.query_to_models(t.symbol, q.results, Quote)
        except Exception as e:
            print "{} : exception {}".format(t.symbol, e)

if __name__ == '__main__':
    # sparse_entries()
    # historic_entries()
    ticker_entries()
    #add_sg_quote()

    #t= Ticker.objects.get()
    #print t.quote_set.get().change_inpercent
    #print t.quote_set.get().market_cap

    #from ticker.query import QueryInterface
    #print t

    #pull_sg_quotes()
