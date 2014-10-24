import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks.settings')

from ticker.models import Ticker, Quote, Historical
from ticker.query import QueryInterface
from common.utils import get_field_verbose_names
from common.utils import get_fields

import datetime


def sparse_entries():
    """ add one ticker and a couple of quotes """

    # add one ticker
    tick = Ticker.objects.get_or_create(symbol="GOOG",
                                        name="Google Inc",
                                        industry="internet",
                                        industry_id=100)[0]

    print tick.id
    print Ticker.objects.all()

    # add a couple of quotes
    tick.quote_set.create(date=datetime.date(2014, 10, 24),  # yr, mt, day
                          time=datetime.time(8, 20, 30),  # hr, min, sec
                          change=+0.1,
                          ask=582.1)

    tick.quote_set.create(date=datetime.date(2014, 10, 24),  # yr, mt, day
                          time=datetime.time(10, 20, 30),  # hr, min, sec
                          change=-0.81,
                          ask=582.65)

    tick.quote_set.create(date=datetime.date(2014, 10, 25),  # yr, mt, day
                          time=datetime.time(10, 20, 30),  # hr, min, sec
                          change=+0.6,
                          ask=583)

    print tick.quote_set.all()  # get allthe quotes with ticker=tick
    print Quote.objects.filter(ticker__symbol='GOOG')  # ticker is Foreign key
    print Quote.objects.filter(date__day=25)


def historic_entries():
    """ add some historic entries """

    Ticker.objects.get(symbol='GOOG')
    query_results = QueryInterface.query_historicaldata("*", "GOOG")
    Ticker.query_to_models('GOOG', query_results.results, model=Historical)


def ticker_entries(company_filter_tag=None):
    """ download tickers (apply company_filter_tag if specified) """

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


def add_sg_quote():
    """ add an arbitrary SG quote for testing """

    # add ticker
    ticker = 'S68.SI'  # singapore exchange

    # query quote
    q = QueryInterface.query_quote(','.join(get_field_verbose_names(Quote)),
                                   ticker)

    # add quote to ticker
    Ticker.query_to_models(ticker, q, Quote)


def pull_sg_quotes():
    """ search through all tickers in SG market and pull them off the web """

    # go for SG tickers
    for t in Ticker.objects.filter(symbol__contains='.SI').all():
        q = QueryInterface.query_quote(','.join(get_field_verbose_names(Quote)),
                                       t.symbol)
        try:
            Ticker.query_to_models(t.symbol, q, Quote)
            QueryInterface.time_stamp(q.results)
            print q.results[0]
            print """
                  {}: quote D:{} T:{} successfull added!
                  """.format(t.symbol,
                             q.results[0]['date'],
                             q.results[0]['time'])
        except Exception as e:
            print "{} : caught exception! : {}".format(t.symbol, e)


def top_five_most_quotes():
    """ print the top 5 tickers with the most quotes """
    # TODO : broken?

    for ticker in sorted([(len(t.quote_set.all()), t)
                          for t in Ticker.objects.all()],
                         reverse=True)[:5]:
        print ticker[1].quote_set.all()


def test_pandas():

    ticker = 'S68.SI'  # singapore exchange

    # q = QueryInterface.query_historicaldata("Volume,Open,Close,Date",
    #                                         ticker)

    # print q.to_pandas()

    q = QueryInterface.query_quote(','.join(get_field_verbose_names(Quote)),
                                   ticker)

    # print q.to_pandas()

    df = q.to_pandas()
    for f in get_fields(Quote, name_filter_list=df.columns):
        df[f.verbose_name] = df[f.verbose_name].map(lambda x: f.to_python(x))

    print df['LastTradeDate']


def pandas_to_db(pickle_filename):
    """ unpickle the pandas file from the db and load the data into
    the database"""
    import pickle

    df = pickle.load(open(pickle_filename, 'rb'))

    def ticker_portion(df):
        # get the ticker part

        field_names = get_fields(Ticker,
                                 attr_func=lambda x: x.name,
                                 filt_func=lambda x: x.name,
                                 name_filter_list=df.columns)

        return df[field_names].drop_duplicates()

    def quote_portion(df):
        # get the Quote fields that are in dataframe colums
        field_names = get_fields(Quote,
                                 attr_func=lambda x: x.name,
                                 filt_func=lambda x: x.name,
                                 name_filter_list=df.columns)

        # I need to include 'ticker_id' here because its a Foreign Key Field
        # and the name is different (i.e. 'ticker') in Quote
        field_names += ['ticker_id', ]
        df = df[field_names]

        # TODO : I changed the fields to try the default format if everything
        # fails (so dont need this anymore)
        # need to specially convert date fields since the have been converted to
        # df['last_trade_date'] = df['last_trade_date'].map(
        #    lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

        # this is auto gen anyway
        df.drop('id', axis=1, inplace=True)

        return df

    def insert_to_model(model, df, portion):
        model.objects.all().delete()
        for index, r in portion(df).iterrows():
            # print r
            model.objects.create(**r.to_dict())

    # Ticker
    # insert_to_model(Ticker, df, ticker_portion)
    insert_to_model(Quote, df, quote_portion)


if __name__ == '__main__':
    funcs = {'sparse_entries': sparse_entries,
             'historic_entries': historic_entries,
             'ticker_entries': ticker_entries,
             'add_sg_quote': add_sg_quote,
             'pull_sg_quotes': pull_sg_quotes,
             'top_five_most_quotes': top_five_most_quotes,
             'test_pandas': test_pandas,
             'pandas_to_db': pandas_to_db}

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
