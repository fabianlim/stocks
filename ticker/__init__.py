from ticker.models import Ticker
from ticker.utils import get_quote_data


class DashboardRegistration(object):
    """ to register to the dashboard """

    @staticmethod
    def get_app_main(params):
        return {"template_path": "visual/historic-data.html",
                "args": {"symbol": params['symbol']}}

    @staticmethod
    def get_app_sidebar(params):

        tick = []
        quote = []
        for symbol in params['symbol']:
            # get ticker
            tick += [Ticker.objects.get(symbol=symbol), ]

            # get quote
            quote += [get_quote_data(symbol), ]

        return {"template_path": "visual/ticker-info-sidebar.html",
                "args": {"ticker_quotes": zip(tick, quote)}}
