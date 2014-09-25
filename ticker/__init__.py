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
            quote += [get_quote_data(symbol), ]

        return {"template_path": cur_dir + "/info-sidebar.html",
                "args": {"ticker_quotes": zip(tick, quote)}}

    @staticmethod
    def get_app_main(params):
        return {"template_path": cur_dir + "/historic-data.html",
                "args": {"symbol": params['symbol']}}
