from models import Ticker
from utils import get_quote_data

import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


class DashboardRegistration(object):
    """ to register to the dashboard """

    @staticmethod
    def get_app_sidebar(params):

        tick = []
        quote = []
        for symbol in params['symbol']:
            # get ticker
            tick += [Ticker.objects.get(symbol=symbol), ]

            # get quote
            quote += get_quote_data(symbol)

        return {"template_path": cur_dir + "/info-sidebar.html",
                "args": {"ticker_quotes": zip(tick, quote)}}

    @staticmethod
    def get_app_main(params):
        return {"template_path": cur_dir + "/historic-data.html",
                "args": {"symbol": params['symbol']}}

    @staticmethod
    def get_app_search(params):

        # run the full-text search
        # returns a query set
        search_results = Ticker.objects.search(
            params['?str?'],
            rank_field='relevance',
            headline_document="""name || ', ' ||
                                 industry || ', '
                              """,
            headline_field='headline')

        quotes = get_quote_data([t.symbol for t in search_results])

        # put some quote information
        for r, q in zip(search_results, quotes):
            r.quote = q

        print search_results[0].quote
        # return
        return {"template_path": cur_dir + "/ticker-search.html",
                "args": {"search_results": search_results}}
