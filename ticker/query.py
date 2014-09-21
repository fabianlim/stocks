# Query Interface

from yql import YQLError
from ticker.yahoo_query import run_public_datatables_query
from ticker.models import get_dateformat
from ticker.models import get_fields
from ticker.models import parse_query_result

from django.utils import timezone
from datetime import timedelta


class QueryInterface(object):

    """
    now this only queries Yahoo (using yql) but can be made more general
    in the future.
    Returns a QueryObject
    """
    class QueryObject(object):
        """
        query results packed into this object.
        to_model : helper function to store in Django model
        """
        def __init__(self, results):
            self.count = len(results)
            self.results = results

        def to_model(self, model, **kwargs):
            """ helper function to convert to Django model) """
            for q in self.results:
                parsed = parse_query_result(q,
                                            get_fields(model),
                                            get_dateformat(model))
                try:
                    model.objects.create(**dict(kwargs, **parsed))
                except Exception as e:
                    print """model {} conversion{} failed:
                        parsed as {}""".format(model, q, parsed)
                    print e

    @staticmethod
    def query_quote(fields, symbol):
        """
        method to pull from quotes
        right now this is hard coded to YQL
        """
        # TODO: not good way of handling spaces in "field" input?
        try:
            yql_query = """SELECT {} FROM
                yahoo.finance.quotes
                where symbol='{}'""".format(fields.replace(' ', '_'), symbol)

            return QueryInterface.QueryObject(
                run_public_datatables_query(yql_query).rows)
        except YQLError as e:
            print "Error: query_quote on symbol={}".format(symbol)
            print e

    @staticmethod
    def query_historicaldata(fields,
                             symbol,
                             startDate=timezone.now().date()-timedelta(30),
                             endDate=timezone.now().date()):
        """
        method to pull from historical data
        right now this is hard coded to YQL
        """
        # TODO: not good way of handling spaces in "field" input?
        try:
            yql_query = """SELECT {} FROM
                yahoo.finance.historicaldata
                where symbol='{}'
                AND startDate='{}'
                AND endDate='{}'
                """.format(fields.replace(' ', '_'),
                           symbol,
                           startDate,
                           endDate)

            return QueryInterface.QueryObject(
                run_public_datatables_query(yql_query).rows)
        except YQLError as e:
            print """Error: query_historicaldata on symbol={}
                startDate={} and endDate={}
                """.format(symbol, startDate, endDate)
            print e

    @staticmethod
    def query_tickers(company_filter_tag=None):
        """
        method to oull tickers
        right now this is hard coded to YQL
        """
        # TODO : make filters more general
        try:
            yql_query = """SELECT company, name, id FROM
                yahoo.finance.industry
                WHERE (id IN
                (SELECT industry.id FROM
                yahoo.finance.sectors))
                """
            # add filter tag if present
            if company_filter_tag and isinstance(company_filter_tag,
                                                 basestring):
                yql_query += " AND company.symbol LIKE '{}'".format(
                    company_filter_tag)

            # each row is an industry's worth of tickers
            return run_public_datatables_query(yql_query).rows
        except YQLError as e:
            print e

    # returns the date and time
    # input is a dictionary of results
    @staticmethod
    def time_stamp(results):
        now = timezone.now()
        for r in results:
            r['date'] = now.date()  # will timestamp with server time
            r['time'] = now.time()
