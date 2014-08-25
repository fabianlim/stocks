import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks.settings')

from django.db import models
from ticker.models import Ticker, Quote

import datetime

def sparse_entries():
# main will not really run because of paths problems
# add the ticker
    tick =Ticker.objects.get_or_create(name="GOOG")[0]

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
    print Quote.objects.filter(ticker__name='GOOG') # ticker is Foreign key here
    print Quote.objects.filter(date__day=25)

def historic_entries():
    tick = Ticker.objects.get(name='GOOG')
    from ticker.query import QueryInterface
    query_results = QueryInterface.query_historicaldata("*", "GOOG")
    Ticker.query_to_models('GOOG', query_results.results)

if __name__ == '__main__':
     sparse_entries()
    #historic_entries()
